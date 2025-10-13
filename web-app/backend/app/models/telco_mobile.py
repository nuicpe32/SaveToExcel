from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class TelcoMobile(Base):
    """Model สำหรับผู้ให้บริการเครือข่ายโทรศัพท์มือถือ"""
    __tablename__ = "telco_mobile"

    id = Column(Integer, primary_key=True, index=True)

    # Company Information
    company_name = Column(String(255), nullable=False, unique=True, index=True)
    company_name_short = Column(String(100), index=True)  # ชื่อย่อ เช่น "AIS", "True", "dtac"

    # Address Information
    building_name = Column(String(255))  # ชื่ออาคาร
    company_address = Column(String(255))  # เลขที่
    soi = Column(String(100))
    moo = Column(String(50))
    road = Column(String(100))
    sub_district = Column(String(100))  # แขวง/ตำบล
    district = Column(String(100))      # เขต/อำเภอ
    province = Column(String(100))
    postal_code = Column(String(10))

    # Contact Information
    phone = Column(String(50))
    email = Column(String(100))
    website = Column(String(255))

    # Status
    is_active = Column(Boolean, default=True, index=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    telco_mobile_accounts = relationship("TelcoMobileAccount", back_populates="telco_mobile")

