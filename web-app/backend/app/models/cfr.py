from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, BigInteger, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class CFR(Base):
    """Model สำหรับ Central Fraud Registry - ข้อมูลเส้นทางการเงิน"""
    __tablename__ = "cfr"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id", ondelete="CASCADE"), nullable=False, index=True)

    # File Information
    filename = Column(String(255), nullable=False, index=True)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())

    # CFR Response Data
    response_id = Column(BigInteger)
    bank_case_id = Column(String(100), index=True)
    timestamp_insert = Column(String(50))

    # From Account (ต้นทาง)
    from_bank_code = Column(Integer)
    from_bank_short_name = Column(String(50))
    from_account_no = Column(String(50), index=True)
    from_account_name = Column(String(255))

    # To Account (ปลายทาง)
    to_bank_code = Column(Integer)
    to_bank_short_name = Column(String(50))
    to_bank_branch = Column(String(100))
    to_id_type = Column(String(50))
    to_id = Column(String(50))
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(50))

    # PromptPay Information
    promptpay_type = Column(String(50))
    promptpay_id = Column(String(50))

    # To Account Details
    to_account_no = Column(String(50), index=True)
    to_account_name = Column(String(255))
    to_account_status = Column(String(50))
    to_open_date = Column(String(50))
    to_close_date = Column(String(50))
    to_balance = Column(DECIMAL(15, 2))

    # Transfer Information
    transfer_date = Column(String(50), index=True)
    transfer_channel = Column(String(100))
    transfer_channel_detail = Column(String(255))
    transfer_time = Column(String(50))
    transfer_amount = Column(DECIMAL(15, 2))
    transfer_description = Column(Text)
    transfer_ref = Column(String(100))

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer)

    # Relationships
    criminal_case = relationship("CriminalCase", back_populates="cfr_records")

