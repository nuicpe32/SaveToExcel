from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class NonBankAccount(Base):
    """
    Model สำหรับหมายเรียกผู้ให้บริการที่ไม่ใช่ธนาคาร (Non-Bank)
    เช่น TrueMoney, AirPay, Rabbit LINE Pay, etc.
    """
    __tablename__ = "non_bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id", ondelete="CASCADE"), nullable=False, index=True)
    non_bank_id = Column(Integer, ForeignKey("non_banks.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # ข้อมูลเอกสาร
    order_number = Column(Integer)
    document_number = Column(String(100))
    document_date = Column(Date)
    document_date_thai = Column(String(100))
    
    # ข้อมูลผู้ให้บริการและบัญชี
    provider_name = Column(String(255), nullable=False, index=True)  # ชื่อผู้ให้บริการ
    account_number = Column(String(100), nullable=False)              # เลขที่บัญชี/หมายเลข
    account_name = Column(String(255))                                # ชื่อบัญชี
    account_owner = Column(String(255))                               # เจ้าของบัญชี
    
    # ข้อมูลคดี
    complainant = Column(String(255))      # ผู้กล่าวหา/ผู้เสียหาย
    victim_name = Column(String(255))      # deprecated - ใช้ complainant แทน
    case_id = Column(String(100))          # เลขคดี
    
    # ช่วงเวลาที่ต้องการข้อมูล
    time_period = Column(String(255))      # ช่วงเวลาที่ทำธุรกรรม
    
    # การส่งหมายเรียก
    delivery_date = Column(Date)           # กำหนดส่ง
    delivery_month = Column(String(50), index=True)  # เดือนที่กำหนดส่ง
    delivery_time = Column(String(20))     # เวลาที่กำหนดส่ง
    
    # สถานะ
    reply_status = Column(Boolean, default=False, index=True)  # สถานะตอบกลับ
    status = Column(String(50), default='pending')             # สถานะทั่วไป
    
    # การอายัด
    is_frozen = Column(Boolean, default=False)  # อายัดหรือไม่
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    
    # Relationships
    criminal_case = relationship("CriminalCase", back_populates="non_bank_accounts")
    non_bank = relationship("NonBank", back_populates="non_bank_accounts")
    creator = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<NonBankAccount(id={self.id}, provider={self.provider_name}, account={self.account_number})>"

