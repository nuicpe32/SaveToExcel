from sqlalchemy import Column, Integer, String, DateTime, Text, Date, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    bank_id = Column(Integer, ForeignKey("banks.id", ondelete="SET NULL"), index=True)

    # Document Information
    order_number = Column(Integer, index=True)
    document_number = Column(String, index=True)
    document_date = Column(Date)
    document_date_thai = Column(String)  # วันที่ในรูปแบบไทย เช่น "11 เม.ย. 66"

    # Bank Information
    bank_name = Column(String, nullable=False, index=True)
    account_number = Column(String, nullable=False, index=True)
    account_name = Column(String, nullable=False)

    # Additional Information
    time_period = Column(String)  # ช่วงเวลาที่ทำธุรกรรม
    
    # Note: Bank address is now retrieved from banks table via bank_id FK
    # Documents are sent to headquarters only (no branch field needed)

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
    criminal_case = relationship("CriminalCase", back_populates="bank_accounts")
    bank = relationship("Bank", back_populates="bank_accounts")