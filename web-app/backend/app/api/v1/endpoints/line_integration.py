from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.services.line_service import LineService

router = APIRouter()

@router.get("/auth-url")
async def get_line_auth_url(current_user: User = Depends(get_current_user)):
    auth_url = LineService.generate_auth_url(current_user.id)
    return {"auth_url": auth_url}

@router.get("/callback")
async def line_callback(
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        result = await LineService.handle_callback(code, state, db)
        return RedirectResponse(url="http://localhost:3001/profile?line=success")
    except Exception as e:
        return RedirectResponse(url=f"http://localhost:3001/profile?line=error&message={str(e)}")

@router.get("/status")
async def get_line_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    line_account = LineService.get_user_line_account(current_user.id, db)
    if not line_account:
        return {"connected": False}

    return {
        "connected": True,
        "line_display_name": line_account.line_display_name,
        "line_picture_url": line_account.line_picture_url,
        "is_active": line_account.is_active,
        "linked_at": line_account.linked_at.isoformat() if line_account.linked_at else None,
        "notify_new_case": line_account.notify_new_case,
        "notify_case_update": line_account.notify_case_update,
        "notify_summons_sent": line_account.notify_summons_sent,
        "notify_email_opened": line_account.notify_email_opened,
    }

@router.put("/preferences")
async def update_notification_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = LineService.update_preferences(current_user.id, preferences, db)
    return result

@router.delete("/disconnect")
async def disconnect_line(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = LineService.disconnect(current_user.id, db)
    return result

@router.post("/test-notification")
async def send_test_notification(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = await LineService.send_notification(
        user_id=current_user.id,
        notification_type="connection_test",
        title="🔔 ทดสอบการแจ้งเตือน",
        message="นี่คือข้อความทดสอบจากระบบ CCMS\n\nถ้าคุณเห็นข้อความนี้แสดงว่าระบบการแจ้งเตือนทำงานปกติ",
        db=db
    )

    if success:
        return {"success": True, "message": "ส่งการแจ้งเตือนทดสอบสำเร็จ"}
    else:
        raise HTTPException(status_code=400, detail="ไม่สามารถส่งการแจ้งเตือนได้")

@router.get("/notification-history")
async def get_notification_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    logs = LineService.get_notification_history(current_user.id, db, limit)
    return {"logs": logs}
