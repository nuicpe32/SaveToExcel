from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Bank(Base):
    """Bank master data model"""
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String(255), unique=True, nullable=False, index=True)
    bank_code = Column(String(10), index=True)
    bank_short_name = Column(String(20), index=True)
    bank_address = Column(String(500))
    soi = Column(String(100))
    moo = Column(String(50))
    road = Column(String(100))
    sub_district = Column(String(100))
    district = Column(String(100))
    province = Column(String(100))
    postal_code = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    bank_accounts = relationship("BankAccount", back_populates="bank")
