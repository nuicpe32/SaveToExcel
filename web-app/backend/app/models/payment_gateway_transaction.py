from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class PaymentGatewayTransaction(Base):
    """
    Model สำหรับรายละเอียดการโอนเงิน Payment Gateway
    เก็บข้อมูลการโอนเงินจากบัญชีต้นทางไปยังบัญชี Payment Gateway ปลายทาง
    """
    __tablename__ = "payment_gateway_transactions"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    payment_gateway_account_id = Column(Integer, ForeignKey("payment_gateway_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # บัญชีต้นทาง (Source Account)
    source_bank_id = Column(Integer, ForeignKey("banks.id", ondelete="SET NULL"), nullable=True, index=True)  # ธนาคารต้นทาง (FK)
    source_account_number = Column(String(100))  # เลขที่บัญชีต้นทาง
    source_account_name = Column(String(255))  # ชื่อบัญชีต้นทาง
    
    # บัญชีปลายทาง (Destination Account) - ดึงจาก payment_gateway_accounts
    destination_bank_id = Column(Integer, ForeignKey("banks.id", ondelete="SET NULL"), nullable=True, index=True)  # ธนาคารปลายทาง (FK)
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
    criminal_case = relationship("CriminalCase", backref="payment_gateway_transactions")
    payment_gateway_account = relationship("PaymentGatewayAccount", backref="transactions")
    source_bank = relationship("Bank", foreign_keys=[source_bank_id])
    destination_bank = relationship("Bank", foreign_keys=[destination_bank_id])
    creator = relationship("User", foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<PaymentGatewayTransaction(id={self.id}, amount={self.transfer_amount}, date={self.transfer_date})>"

