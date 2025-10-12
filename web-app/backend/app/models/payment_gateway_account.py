from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class PaymentGatewayAccount(Base):
    """
    Model สำหรับหมายเรียกผู้ให้บริการ Payment Gateway
    เช่น Omise, GB Prime Pay, 2C2P
    """
    __tablename__ = "payment_gateway_accounts"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    payment_gateway_id = Column(Integer, ForeignKey("payment_gateways.id", ondelete="SET NULL"), nullable=True, index=True)
    bank_id = Column(Integer, ForeignKey("banks.id", ondelete="SET NULL"), nullable=True, index=True)  # ธนาคารที่เปิดบัญชี
    
    # ข้อมูลเอกสาร
    document_number = Column(String(100))
    document_date = Column(Date)
    
    # ข้อมูลบัญชี
    account_number = Column(String(100), nullable=False)  # เลขที่บัญชี/หมายเลข
    account_name = Column(String(255))                    # ชื่อบัญชี
    
    # ช่วงเวลาที่ต้องการข้อมูล
    time_period = Column(String(255))  # ช่วงเวลาที่ทำธุรกรรม
    
    # การส่งหมายเรียก
    delivery_date = Column(Date)  # กำหนดส่ง
    
    # สถานะ
    reply_status = Column(Boolean, default=False, index=True)  # สถานะตอบกลับ
    status = Column(String(50), default='pending')             # สถานะทั่วไป
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    
    # Relationships
    criminal_case = relationship("CriminalCase", backref="payment_gateway_accounts")
    payment_gateway = relationship("PaymentGateway", backref="payment_gateway_accounts")
    bank = relationship("Bank", foreign_keys=[bank_id])
    creator = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<PaymentGatewayAccount(id={self.id}, account={self.account_number})>"

