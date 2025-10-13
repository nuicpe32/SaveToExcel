from sqlalchemy import Column, Integer, String, DateTime, Text, Date, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class TelcoMobileAccount(Base):
    """Model สำหรับข้อมูลหมายเลขโทรศัพท์ที่เกี่ยวข้องกับคดี"""
    __tablename__ = "telco_mobile_accounts"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    telco_mobile_id = Column(Integer, ForeignKey("telco_mobile.id", ondelete="SET NULL"), index=True)

    # Document Information
    order_number = Column(Integer, index=True)
    document_number = Column(String, index=True)
    document_date = Column(Date)

    # Telco Information
    provider_name = Column(String, nullable=False, index=True)  # ชื่อผู้ให้บริการ
    phone_number = Column(String, nullable=False, index=True)   # หมายเลขโทรศัพท์

    # Additional Information
    time_period = Column(String)  # ช่วงเวลาที่ขอข้อมูล

    # Delivery Information
    delivery_date = Column(Date)  # กำหนดให้ส่งเอกสาร

    # Status and Response
    reply_status = Column(Boolean, default=False, index=True)
    days_since_sent = Column(Integer)

    # Additional Information
    notes = Column(Text)
    status = Column(String, default="pending", index=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer)

    # Relationships
    criminal_case = relationship("CriminalCase", back_populates="telco_mobile_accounts")
    telco_mobile = relationship("TelcoMobile", back_populates="telco_mobile_accounts")

