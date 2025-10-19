#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Endpoints สำหรับ Email Tracking (ตรวจสอบว่าผู้รับเปิดอ่านหรือยัง)
"""

from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
import io

from app.core.database import get_db
from app.models.email_log import EmailLog

router = APIRouter()

# Tracking pixel (1x1 transparent GIF)
TRACKING_PIXEL = bytes.fromhex('47494638396101000100800000000000ffffff21f90401000000002c00000000010001000002024401003b')

@router.get("/track/{email_log_id}.gif")
async def track_email_open(
    email_log_id: int,
    db: Session = Depends(get_db)
):
    """
    Email tracking endpoint - ใช้ tracking pixel (1x1 transparent GIF)
    
    เมื่อผู้รับเปิดอีเมล์ email client จะโหลดรูปนี้
    และเราจะบันทึกว่าผู้รับเปิดอ่านแล้ว
    
    Usage in HTML email:
    <img src="http://backend-url/api/v1/email-tracking/track/{email_log_id}.gif" width="1" height="1" />
    """
    try:
        # หา email log
        email_log = db.query(EmailLog).filter(EmailLog.id == email_log_id).first()
        
        if email_log:
            # อัปเดต opened count และ timestamp
            email_log.opened_count = (email_log.opened_count or 0) + 1
            email_log.opened_at = datetime.now()
            
            # ถ้าเปิดครั้งแรก ให้บันทึก opened_at
            if email_log.opened_count == 1:
                email_log.opened_at = datetime.now()
            
            db.commit()
            
            print(f"📧 Email opened: log_id={email_log_id}, count={email_log.opened_count}")
        
        # Return tracking pixel (1x1 transparent GIF)
        return StreamingResponse(
            io.BytesIO(TRACKING_PIXEL),
            media_type="image/gif",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except Exception as e:
        print(f"Error in email tracking: {e}")
        # แม้เกิด error ก็ส่ง pixel กลับไปเพื่อไม่ให้ email client แสดง broken image
        return StreamingResponse(
            io.BytesIO(TRACKING_PIXEL),
            media_type="image/gif"
        )

@router.get("/track-link/{email_log_id}/{link_id}")
async def track_link_click(
    email_log_id: int,
    link_id: str,
    db: Session = Depends(get_db)
):
    """
    Link tracking endpoint - บันทึกเมื่อผู้รับคลิก link ในอีเมล์
    
    Note: ฟีเจอร์นี้สำหรับอนาคต (ยังไม่ได้ใช้)
    """
    try:
        email_log = db.query(EmailLog).filter(EmailLog.id == email_log_id).first()
        
        if email_log:
            # บันทึกว่าผู้รับคลิก link
            # TODO: สร้าง table สำหรับบันทึก link clicks
            print(f"🔗 Link clicked: email_log_id={email_log_id}, link_id={link_id}")
        
        # Redirect ไปยัง URL ที่ต้องการ (สำหรับอนาคต)
        return {"message": "Link tracking recorded"}
        
    except Exception as e:
        print(f"Error in link tracking: {e}")
        return {"message": "Error"}

