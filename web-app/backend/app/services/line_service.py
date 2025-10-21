import httpx
import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional

from app.core.config import settings
from app.models.line_account import LineAccount
from app.models.line_notification_log import LineNotificationLog
from app.core.encryption import encrypt_token, decrypt_token

class LineService:
    LINE_AUTH_URL = "https://access.line.me/oauth2/v2.1/authorize"
    LINE_TOKEN_URL = "https://api.line.me/oauth2/v2.1/token"
    LINE_PROFILE_URL = "https://api.line.me/v2/profile"
    LINE_MESSAGE_URL = "https://api.line.me/v2/bot/message/push"

    @staticmethod
    def generate_auth_url(user_id: int) -> str:
        state = f"{user_id}:{secrets.token_urlsafe(32)}"

        params = {
            "response_type": "code",
            "client_id": settings.LINE_CHANNEL_ID,
            "redirect_uri": settings.LINE_CALLBACK_URL,
            "state": state,
            "scope": "profile openid",
        }

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{LineService.LINE_AUTH_URL}?{query_string}"

    @staticmethod
    async def handle_callback(code: str, state: str, db: Session) -> dict:
        try:
            user_id = int(state.split(":")[0])
        except:
            raise HTTPException(status_code=400, detail="Invalid state parameter")

        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                LineService.LINE_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": settings.LINE_CALLBACK_URL,
                    "client_id": settings.LINE_CHANNEL_ID,
                    "client_secret": settings.LINE_CHANNEL_SECRET,
                }
            )

            if token_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get access token")

            token_data = token_response.json()

        access_token = token_data["access_token"]

        async with httpx.AsyncClient() as client:
            profile_response = await client.get(
                LineService.LINE_PROFILE_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )

            if profile_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user profile")

            profile_data = profile_response.json()

        line_account = db.query(LineAccount).filter_by(user_id=user_id).first()

        if line_account:
            line_account.line_user_id = profile_data["userId"]
            line_account.line_display_name = profile_data["displayName"]
            line_account.line_picture_url = profile_data.get("pictureUrl")
            line_account.line_status_message = profile_data.get("statusMessage")
            line_account.access_token = encrypt_token(access_token)
            line_account.refresh_token = encrypt_token(token_data.get("refresh_token", ""))
            line_account.token_expires_at = datetime.now() + timedelta(seconds=token_data.get("expires_in", 2592000))
            line_account.is_active = True
            line_account.linked_at = datetime.now()
        else:
            line_account = LineAccount(
                user_id=user_id,
                line_user_id=profile_data["userId"],
                line_display_name=profile_data["displayName"],
                line_picture_url=profile_data.get("pictureUrl"),
                line_status_message=profile_data.get("statusMessage"),
                access_token=encrypt_token(access_token),
                refresh_token=encrypt_token(token_data.get("refresh_token", "")),
                token_expires_at=datetime.now() + timedelta(seconds=token_data.get("expires_in", 2592000))
            )
            db.add(line_account)

        db.commit()
        db.refresh(line_account)

        await LineService.send_notification(
            user_id=user_id,
            notification_type="connection_test",
            title="🎉 เชื่อมต่อ LINE สำเร็จ!",
            message=f"ยินดีต้อนรับคุณ {profile_data['displayName']} เข้าสู่ระบบ CCMS\n\nบัญชี LINE ของคุณได้เชื่อมต่อกับระบบจัดการคดีอาญาเรียบร้อยแล้ว คุณจะได้รับการแจ้งเตือนสำคัญผ่าน LINE นี้ต่อไป",
            db=db
        )

        return {"success": True, "message": "เชื่อมต่อ LINE สำเร็จ"}

    @staticmethod
    def get_user_line_account(user_id: int, db: Session) -> Optional[LineAccount]:
        return db.query(LineAccount).filter_by(user_id=user_id, is_active=True).first()

    @staticmethod
    async def send_notification(
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        db: Session,
        criminal_case_id: Optional[int] = None
    ) -> bool:
        line_account = LineService.get_user_line_account(user_id, db)
        if not line_account:
            return False

        preference_map = {
            "connection_test": True,
            "new_case": line_account.notify_new_case,
            "case_update": line_account.notify_case_update,
            "summons_sent": line_account.notify_summons_sent,
            "email_opened": line_account.notify_email_opened,
        }

        if not preference_map.get(notification_type, False):
            return False

        log = LineNotificationLog(
            line_account_id=line_account.id,
            notification_type=notification_type,
            title=title,
            message=message,
            criminal_case_id=criminal_case_id,
            status="pending"
        )
        db.add(log)
        db.commit()

        try:
            full_message = f"{title}\n\n{message}"

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    LineService.LINE_MESSAGE_URL,
                    headers={
                        "Authorization": f"Bearer {settings.LINE_CHANNEL_ACCESS_TOKEN}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "to": line_account.line_user_id,
                        "messages": [{
                            "type": "text",
                            "text": full_message
                        }]
                    },
                    timeout=10.0
                )

            if response.status_code == 200:
                log.status = "sent"
                log.sent_at = datetime.now()
                line_account.last_used_at = datetime.now()
            else:
                log.status = "failed"
                log.error_message = f"HTTP {response.status_code}: {response.text}"

            db.commit()
            return response.status_code == 200

        except Exception as e:
            log.status = "failed"
            log.error_message = str(e)
            db.commit()
            return False

    @staticmethod
    def update_preferences(user_id: int, preferences: dict, db: Session) -> dict:
        line_account = LineService.get_user_line_account(user_id, db)
        if not line_account:
            raise HTTPException(status_code=404, detail="LINE account not found")

        if "notify_new_case" in preferences:
            line_account.notify_new_case = preferences["notify_new_case"]
        if "notify_case_update" in preferences:
            line_account.notify_case_update = preferences["notify_case_update"]
        if "notify_summons_sent" in preferences:
            line_account.notify_summons_sent = preferences["notify_summons_sent"]
        if "notify_email_opened" in preferences:
            line_account.notify_email_opened = preferences["notify_email_opened"]

        db.commit()
        return {"success": True, "message": "อัปเดตการตั้งค่าสำเร็จ"}

    @staticmethod
    def disconnect(user_id: int, db: Session) -> dict:
        line_account = db.query(LineAccount).filter_by(user_id=user_id).first()
        if line_account:
            db.delete(line_account)
            db.commit()

        return {"success": True, "message": "ยกเลิกการเชื่อมต่อสำเร็จ"}

    @staticmethod
    def get_notification_history(user_id: int, db: Session, limit: int = 50):
        line_account = db.query(LineAccount).filter_by(user_id=user_id).first()
        if not line_account:
            return []

        logs = db.query(LineNotificationLog).filter_by(
            line_account_id=line_account.id
        ).order_by(
            LineNotificationLog.created_at.desc()
        ).limit(limit).all()

        return [{
            "id": log.id,
            "notification_type": log.notification_type,
            "title": log.title,
            "message": log.message,
            "status": log.status,
            "error_message": log.error_message,
            "sent_at": log.sent_at.isoformat() if log.sent_at else None,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        } for log in logs]

    @staticmethod
    async def send_summons_notification(
        user_id: int,
        account_type: str,
        account_data: dict,
        criminal_case: dict,
        db: Session,
        updated_by_user: dict = None
    ) -> bool:
        """
        ส่งการแจ้งเตือนเมื่อได้รับข้อมูลตอบกลับจากหมายเรียก

        Args:
            user_id: ID ของผู้ใช้ที่จะรับการแจ้งเตือน
            account_type: ประเภทบัญชี (bank, non_bank, payment_gateway, telco_mobile, telco_internet, suspect)
            account_data: ข้อมูลบัญชีที่ส่งหมายเรียก
            criminal_case: ข้อมูลคดี
            db: Database session
            updated_by_user: ข้อมูลผู้อัปเดตสถานะ (rank, full_name)
        """

        # สร้างข้อความแจ้งเตือนตามประเภท
        emoji_map = {
            "bank": "🏦",
            "non_bank": "🏪",
            "payment_gateway": "💳",
            "telco_mobile": "📱",
            "telco_internet": "🌐",
            "suspect": "👤"
        }

        type_name_map = {
            "bank": "บัญชีธนาคาร",
            "non_bank": "Non-Bank",
            "payment_gateway": "Payment Gateway",
            "telco_mobile": "หมายเลขโทรศัพท์",
            "telco_internet": "IP Address",
            "suspect": "ผู้ต้องหา"
        }

        emoji = emoji_map.get(account_type, "📄")
        type_name = type_name_map.get(account_type, account_type)

        # สร้างหัวข้อ
        title = f"{emoji} อัพเดตสถานะข้อมูลหมายเรียก{type_name}"

        # สร้างข้อความรายละเอียด
        message_parts = []

        # ข้อมูลคดี
        case_id = criminal_case.get('case_id') or criminal_case.get('case_number', '-')
        victim = criminal_case.get('victim_name') or criminal_case.get('complainant', '-')
        message_parts.append(f"📋 คดีหมายเลข: {case_id}")
        message_parts.append(f"👥 ผู้เสียหาย: {victim}")
        message_parts.append("")

        # ข้อมูลหมายเรียก
        message_parts.append(f"📄 เอกสารหมายเลข: {account_data.get('document_number', '-')}")

        if account_type in ["bank", "non_bank", "payment_gateway"]:
            message_parts.append(f"🏢 สถาบันการเงิน: {account_data.get('provider_name', '-')}")
            message_parts.append(f"💼 ชื่อบัญชี: {account_data.get('account_name', '-')}")
            message_parts.append(f"🔢 เลขที่บัญชี: {account_data.get('account_number', '-')}")
            message_parts.append(f"📅 ช่วงเวลา: {account_data.get('time_period', '-')}")

        elif account_type == "telco_mobile":
            message_parts.append(f"🏢 ผู้ให้บริการ: {account_data.get('provider_name', '-')}")
            message_parts.append(f"📞 หมายเลข: {account_data.get('phone_number', '-')}")
            message_parts.append(f"📅 ช่วงเวลา: {account_data.get('time_period', '-')}")

        elif account_type == "telco_internet":
            message_parts.append(f"🏢 ผู้ให้บริการ: {account_data.get('provider_name', '-')}")
            message_parts.append(f"🌐 IP Address: {account_data.get('ip_address', '-')}")
            message_parts.append(f"🕒 วันเวลาที่ใช้: {account_data.get('datetime_used', '-')}")

        elif account_type == "suspect":
            message_parts.append(f"👤 ชื่อผู้ต้องหา: {account_data.get('name', '-')}")
            message_parts.append(f"🆔 เลขบัตรประชาชน: {account_data.get('national_id', '-')}")
            if account_data.get('address'):
                message_parts.append(f"📍 ที่อยู่: {account_data.get('address', '-')}")

        # ข้อมูลผู้ส่ง
        message_parts.append("")
        if account_data.get('recipient_email'):
            message_parts.append(f"📧 ส่งไปที่: {account_data.get('recipient_email')}")
        message_parts.append(f"✅ สถานะ: ได้รับข้อมูลแล้ว")

        # ข้อมูลผู้อัพเดตสถานะ
        if updated_by_user:
            rank = updated_by_user.get('rank', '')
            full_name = updated_by_user.get('full_name', '')
            if rank or full_name:
                message_parts.append(f"👤 ผู้อัพเดตสถานะ: {rank} {full_name}".strip())

        message = "\n".join(message_parts)

        # ส่งการแจ้งเตือน
        return await LineService.send_notification(
            user_id=user_id,
            notification_type="summons_sent",
            title=title,
            message=message,
            db=db,
            criminal_case_id=criminal_case.get('id')
        )
