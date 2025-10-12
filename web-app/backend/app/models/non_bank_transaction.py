from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class NonBankTransaction(Base):
    """
    Model สำหรับรายละเอียดการโอนเงิน Non-Bank
    เก็บข้อมูลการโอนเงินจากบัญชีต้นทางไปยังบัญชี Non-Bank ปลายทาง
    """
    __tablename__ = "non_bank_transactions"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    non_bank_account_id = Column(Integer, ForeignKey("non_bank_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # บัญชีต้นทาง (Source Account)
    source_bank_id = Column(Integer, ForeignKey("banks.id", ondelete="SET NULL"), nullable=True, index=True)  # ธนาคารต้นทาง (FK)
    source_account_number = Column(String(100))  # เลขที่บัญชีต้นทาง
    source_account_name = Column(String(255))  # ชื่อบัญชีต้นทาง
    
    # บัญชีปลายทาง (Destination Account) - ดึงจาก non_bank_accounts
    destination_non_bank_id = Column(Integer, ForeignKey("non_banks.id", ondelete="SET NULL"), nullable=True, index=True)  # ผู้ให้บริการปลายทาง (FK)
    destination_account_number = Column(String(100))  # เลขที่บัญชีปลายทาง
    destination_account_name = Column(String(255))  # ชื่อบัญชีปลายทาง
    
    # ข้อมูลการโอน
    transfer_date = Column(Date, index=True)  # วันที่โอน
    transfer_time = Column(String(20))  # เวลาที่โอน (HH:MM)
    transfer_amount = Column(Numeric(15, 2))  # จำนวนเงินที่โอน
    
    # หมายเหตุเพิ่มเติม
    note = Column(String(500))  # หมายเหตุ (ถ้ามี)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    
    # Relationships
    criminal_case = relationship("CriminalCase", backref="non_bank_transactions")
    non_bank_account = relationship("NonBankAccount", backref="transactions")
    source_bank = relationship("Bank", foreign_keys=[source_bank_id])
    destination_non_bank = relationship("NonBank", foreign_keys=[destination_non_bank_id])
    creator = relationship("User", foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<NonBankTransaction(id={self.id}, amount={self.transfer_amount}, date={self.transfer_date})>"

