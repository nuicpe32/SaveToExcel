#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Endpoints สำหรับส่งหมายเรียกพยานเอกสารทางอีเมล์
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.models.email_log import EmailLog
from app.models.criminal_case import CriminalCase
from app.models.non_bank_account import NonBankAccount
from app.models.payment_gateway_account import PaymentGatewayAccount
from app.models.telco_mobile_account import TelcoMobileAccount
from app.models.telco_internet_account import TelcoInternetAccount
from app.models.bank_account import BankAccount
from app.models.non_bank import NonBank
from app.models.payment_gateway import PaymentGateway
from app.models.telco_mobile import TelcoMobile
from app.models.telco_internet import TelcoInternet
from app.models.bank import Bank
from app.models.non_bank_transaction import NonBankTransaction
from app.models.payment_gateway_transaction import PaymentGatewayTransaction
from app.schemas.email import EmailSendRequest, EmailSendResponse, EmailLogResponse, EmailHistoryResponse
from app.api.v1.auth import get_current_user
from app.services.email_service import EmailService
from app.services.non_bank_summons_generator import NonBankSummonsGenerator
from app.services.payment_gateway_summons_generator import PaymentGatewaySummonsGenerator
from app.services.telco_mobile_summons_generator import TelcoMobileSummonsGenerator
from app.services.telco_internet_summons_generator import TelcoInternetSummonsGenerator

router = APIRouter()

def get_email_service() -> EmailService:
    """สร้าง EmailService instance จาก configuration"""
    return EmailService(
        smtp_host=settings.SMTP_HOST,
        smtp_port=settings.SMTP_PORT,
        smtp_username=settings.SMTP_USERNAME,
        smtp_password=settings.SMTP_PASSWORD,
        from_email=settings.FROM_EMAIL,
        from_name=settings.FROM_NAME
    )

@router.post("/send-summons", response_model=EmailSendResponse)
def send_summons_email(
    request: EmailSendRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ส่งหมายเรียกพยานเอกสารทางอีเมล์

    รองรับ account_type:
    - non_bank: บัญชีผู้ให้บริการนอกธนาคาร
    - payment_gateway: บัญชีผู้ให้บริการชำระเงิน
    - telco_mobile: หมายเลขโทรศัพท์
    - telco_internet: IP Address
    - bank: บัญชีธนาคาร
    """

    # ตรวจสอบ SMTP configuration
    if not settings.SMTP_USERNAME or not settings.FROM_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email service is not configured. Please configure SMTP settings."
        )

    # ดึงข้อมูลตาม account_type
    account_data = None
    provider_data = None
    criminal_case = None
    html_content = None
    provider_name = None

    try:
        if request.account_type == 'non_bank':
            account_data = db.query(NonBankAccount).filter(
                NonBankAccount.id == request.account_id
            ).first()
            if not account_data:
                raise HTTPException(status_code=404, detail="Non-Bank account not found")

            criminal_case = account_data.criminal_case
            provider_data = db.query(NonBank).filter(
                NonBank.id == account_data.non_bank_id
            ).first()

            # ดึงชื่อผู้ให้บริการจาก relationship
            provider_name = provider_data.company_name if provider_data else 'ไม่ระบุ'

            # ดึงรายการ transactions
            transactions = db.query(NonBankTransaction).filter(
                NonBankTransaction.non_bank_account_id == account_data.id
            ).all()

            # แปลง transactions เป็น dict
            transactions_list = []
            for t in transactions:
                # ดึงชื่อธนาคารจาก relationship
                source_bank_name = ''
                if t.source_bank:
                    source_bank_name = t.source_bank.bank_name
                elif t.source_account_name:
                    source_bank_name = t.source_account_name  # ถ้าไม่มี bank ใช้ชื่อบัญชีแทน

                transactions_list.append({
                    'source_bank_name': source_bank_name,
                    'source_account_number': t.source_account_number or '',
                    'source_account_name': t.source_account_name or '-',  # เพิ่มชื่อบัญชีต้นทาง
                    'transfer_date': t.transfer_date,
                    'transfer_time': t.transfer_time or '',
                    'transfer_amount': t.transfer_amount
                })

            # สร้าง HTML หมายเรียก (พร้อมลายเซ็นสำหรับอีเมล์)
            generator = NonBankSummonsGenerator()
            html_content = generator.generate_bank_letter_html(
                bank_data={
                    'document_number': account_data.document_number,
                    'document_date': account_data.document_date,
                    'provider_name': provider_name,
                    'account_number': account_data.account_number,
                    'account_name': account_data.account_name,
                    'time_period': account_data.time_period
                },
                criminal_case={
                    'victim_name': criminal_case.complainant if criminal_case else '',
                    'case_id': criminal_case.case_id if criminal_case else ''
                },
                freeze_account=request.freeze_account,  # เพิ่มการอายัดบัญชี
                transactions=transactions_list if transactions_list else None,
                signature_path=current_user.signature_path  # เพิ่มลายเซ็นสำหรับอีเมล์
            )

        elif request.account_type == 'payment_gateway':
            account_data = db.query(PaymentGatewayAccount).filter(
                PaymentGatewayAccount.id == request.account_id
            ).first()
            if not account_data:
                raise HTTPException(status_code=404, detail="Payment Gateway account not found")

            criminal_case = account_data.criminal_case
            provider_data = db.query(PaymentGateway).filter(
                PaymentGateway.id == account_data.payment_gateway_id
            ).first()

            # ดึงชื่อผู้ให้บริการจาก relationship
            provider_name = provider_data.company_name if provider_data else 'ไม่ระบุ'

            # ดึงรายการ transactions
            transactions = db.query(PaymentGatewayTransaction).filter(
                PaymentGatewayTransaction.payment_gateway_account_id == account_data.id
            ).all()

            # แปลง transactions เป็น dict
            transactions_list = []
            for t in transactions:
                # ดึงชื่อธนาคารจาก relationship
                source_bank_name = ''
                if t.source_bank:
                    source_bank_name = t.source_bank.bank_name
                elif t.source_account_name:
                    source_bank_name = t.source_account_name  # ถ้าไม่มี bank ใช้ชื่อบัญชีแทน

                transactions_list.append({
                    'source_bank_name': source_bank_name,
                    'source_account_number': t.source_account_number or '',
                    'source_account_name': t.source_account_name or '-',  # เพิ่มชื่อบัญชีต้นทาง
                    'transfer_date': t.transfer_date,
                    'transfer_time': t.transfer_time or '',
                    'transfer_amount': t.transfer_amount
                })

            # สร้าง HTML หมายเรียก
            generator = PaymentGatewaySummonsGenerator()
            html_content = generator.generate_bank_letter_html(
                bank_data={
                    'document_number': account_data.document_number,
                    'document_date': account_data.document_date,
                    'provider_name': provider_name,
                    'account_number': account_data.account_number,
                    'account_name': account_data.account_name,
                    'time_period': account_data.time_period
                },
                criminal_case={
                    'victim_name': criminal_case.complainant if criminal_case else '',
                    'case_id': criminal_case.case_id if criminal_case else ''
                },
                freeze_account=request.freeze_account,  # เพิ่มการอายัดบัญชี
                transactions=transactions_list if transactions_list else None
            )

        elif request.account_type == 'telco_mobile':
            account_data = db.query(TelcoMobileAccount).filter(
                TelcoMobileAccount.id == request.account_id
            ).first()
            if not account_data:
                raise HTTPException(status_code=404, detail="Telco Mobile account not found")

            criminal_case = account_data.criminal_case
            provider_data = db.query(TelcoMobile).filter(
                TelcoMobile.id == account_data.telco_mobile_id
            ).first()

            # ดึงชื่อผู้ให้บริการจาก relationship
            provider_name = provider_data.company_name if provider_data else 'ไม่ระบุ'

            # สร้าง HTML หมายเรียก
            generator = TelcoMobileSummonsGenerator()
            html_content = generator.generate_telco_mobile_letter_html(
                telco_data={
                    'document_number': account_data.document_number,
                    'document_date': account_data.document_date,
                    'provider_name': provider_name,
                    'phone_number': account_data.phone_number,
                    'time_period': account_data.time_period
                },
                criminal_case={
                    'victim_name': criminal_case.complainant if criminal_case else '',
                    'case_id': criminal_case.case_id if criminal_case else ''
                },
                freeze_account=request.freeze_account  # เพิ่มการอายัดบัญชี
            )

        elif request.account_type == 'telco_internet':
            account_data = db.query(TelcoInternetAccount).filter(
                TelcoInternetAccount.id == request.account_id
            ).first()
            if not account_data:
                raise HTTPException(status_code=404, detail="Telco Internet account not found")

            criminal_case = account_data.criminal_case
            provider_data = db.query(TelcoInternet).filter(
                TelcoInternet.id == account_data.telco_internet_id
            ).first()

            # ดึงชื่อผู้ให้บริการจาก relationship
            provider_name = provider_data.company_name if provider_data else 'ไม่ระบุ'

            # สร้าง HTML หมายเรียก
            generator = TelcoInternetSummonsGenerator()
            html_content = generator.generate_telco_internet_letter_html(
                telco_data={
                    'document_number': account_data.document_number,
                    'document_date': account_data.document_date,
                    'provider_name': provider_name,
                    'ip_address': account_data.ip_address,
                    'datetime_used': account_data.datetime_used
                },
                criminal_case={
                    'victim_name': criminal_case.complainant if criminal_case else '',
                    'case_id': criminal_case.case_id if criminal_case else ''
                },
                freeze_account=request.freeze_account  # เพิ่มการอายัดบัญชี
            )

        elif request.account_type == 'bank':
            account_data = db.query(BankAccount).filter(
                BankAccount.id == request.account_id
            ).first()
            if not account_data:
                raise HTTPException(status_code=404, detail="Bank account not found")

            criminal_case = account_data.criminal_case
            provider_data = db.query(Bank).filter(
                Bank.id == account_data.bank_id
            ).first()

            # ดึงชื่อธนาคารจาก account data
            provider_name = account_data.bank_name

            # สำหรับ bank ใช้ generator เดียวกับ non_bank (มี method เดียวกัน)
            generator = NonBankSummonsGenerator()
            html_content = generator.generate_bank_letter_html(
                bank_data={
                    'document_number': account_data.document_number,
                    'document_date': account_data.document_date,
                    'provider_name': provider_name,
                    'account_number': account_data.account_number,
                    'account_name': account_data.account_name,
                    'time_period': account_data.time_period
                },
                criminal_case={
                    'victim_name': criminal_case.complainant if criminal_case else '',
                    'case_id': criminal_case.case_id if criminal_case else ''
                },
                freeze_account=request.freeze_account  # เพิ่มการอายัดบัญชี
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported account_type: {request.account_type}"
            )

        # ตรวจสอบข้อมูล
        if not criminal_case:
            raise HTTPException(status_code=404, detail="Criminal case not found")

        # สร้าง EmailService
        email_service = get_email_service()

        # สร้างชื่อผู้ส่งแบบเต็ม: ยศ + ชื่อ + ตำแหน่ง
        sender_full_name = current_user.full_name
        if current_user.rank:
            sender_full_name = f"{current_user.rank.rank_short}{current_user.full_name}"
        if current_user.position:
            sender_full_name = f"{sender_full_name} {current_user.position}"

        # สร้าง email_log ก่อน เพื่อจะได้มี ID สำหรับ tracking
        email_log = EmailLog(
            account_type=request.account_type,
            account_id=request.account_id,
            criminal_case_id=criminal_case.id,
            recipient_email=request.recipient_email,
            subject=f"หมายเรียกพยานเอกสาร {account_data.document_number} - CaseID {criminal_case.case_id or criminal_case.case_number}",
            document_type=request.document_type,
            status='pending',  # เริ่มต้นเป็น pending
            sent_by=current_user.id,
            retry_count=0
        )
        db.add(email_log)
        db.commit()
        db.refresh(email_log)

        # Debug: ตรวจสอบเบอร์โทรของ user
        print(f"DEBUG: current_user.phone_number = '{current_user.phone_number}'")
        print(f"DEBUG: current_user.email = '{current_user.email}'")
        print(f"DEBUG: current_user.full_name = '{current_user.full_name}'")
        
        # ส่งอีเมล์ พร้อม tracking pixel (ใช้ email_log.id)
        result = email_service.send_summons_email(
            to_email=request.recipient_email,
            provider_name=provider_name or 'ไม่ระบุ',
            document_number=account_data.document_number or '',
            html_content=html_content,
            case_number=criminal_case.case_id or criminal_case.case_number or '',
            account_type=request.account_type,
            sender_name=sender_full_name,  # ยศ + ชื่อ + ตำแหน่ง (แสดงใน From)
            sender_email=current_user.email,  # อีเมล์ของ user (ใช้สำหรับ Reply-To และ CC)
            sender_phone=current_user.phone_number,  # เบอร์โทรของ user
            email_log_id=email_log.id,  # สำหรับ tracking pixel
            backend_url="http://localhost:8000"  # TODO: ใช้จาก settings
        )

        # อัปเดตสถานะ email_log หลังส่งเสร็จ
        email_log.status = result['status']
        email_log.sent_at = datetime.fromisoformat(result['sent_at']) if result['status'] == 'sent' else None
        email_log.error_message = result.get('message') if result['status'] == 'failed' else None
        email_log.pdf_filename = result.get('pdf_filename')
        db.commit()
        db.refresh(email_log)

        # ลบไฟล์ PDF ชั่วคราว (ถ้าต้องการ)
        if result.get('pdf_path'):
            email_service.cleanup_temp_file(result['pdf_path'])

        return EmailSendResponse(
            status=result['status'],
            message=result['message'],
            email_log_id=email_log.id,
            sent_at=email_log.sent_at,
            pdf_filename=result.get('pdf_filename')
        )

    except HTTPException:
        raise
    except Exception as e:
        # บันทึก error log
        if criminal_case:
            error_log = EmailLog(
                account_type=request.account_type,
                account_id=request.account_id,
                criminal_case_id=criminal_case.id,
                recipient_email=request.recipient_email,
                subject=f"หมายเรียกพยานเอกสาร - CaseID {criminal_case.case_id or criminal_case.case_number}",
                document_type=request.document_type,
                status='failed',
                error_message=str(e),
                sent_by=current_user.id,
                retry_count=0
            )
            db.add(error_log)
            db.commit()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending email: {str(e)}"
        )

@router.get("/history/{criminal_case_id}", response_model=EmailHistoryResponse)
def get_email_history(
    criminal_case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    ดึงประวัติการส่งอีเมล์ของคดี
    """
    # ตรวจสอบคดี
    criminal_case = db.query(CriminalCase).filter(CriminalCase.id == criminal_case_id).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")

    # ดึงประวัติการส่งอีเมล์
    total = db.query(EmailLog).filter(EmailLog.criminal_case_id == criminal_case_id).count()
    emails = db.query(EmailLog).filter(
        EmailLog.criminal_case_id == criminal_case_id
    ).order_by(
        EmailLog.created_at.desc()
    ).offset(skip).limit(limit).all()

    return EmailHistoryResponse(
        total=total,
        emails=emails
    )

@router.get("/log/{email_log_id}", response_model=EmailLogResponse)
def get_email_log(
    email_log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ดึงรายละเอียดการส่งอีเมล์
    """
    email_log = db.query(EmailLog).filter(EmailLog.id == email_log_id).first()
    if not email_log:
        raise HTTPException(status_code=404, detail="Email log not found")

    return email_log

@router.get("/by-account/{account_type}/{account_id}", response_model=EmailHistoryResponse)
def get_email_logs_by_account(
    account_type: str,
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    ดึงประวัติการส่งอีเมล์ของ account ที่ระบุ
    
    account_type: non_bank, payment_gateway, telco_mobile, telco_internet, bank
    account_id: ID ของ account
    """
    # นับจำนวนทั้งหมด
    total = db.query(EmailLog).filter(
        EmailLog.account_type == account_type,
        EmailLog.account_id == account_id
    ).count()
    
    # ดึงข้อมูล email logs
    emails = db.query(EmailLog).filter(
        EmailLog.account_type == account_type,
        EmailLog.account_id == account_id
    ).order_by(
        EmailLog.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return EmailHistoryResponse(
        total=total,
        emails=emails
    )