from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Bureau(Base):
    """Model สำหรับหน่วยงานระดับบัญชาการ (บช.)"""
    __tablename__ = "bureaus"

    id = Column(Integer, primary_key=True, index=True)
    name_full = Column(String(255), nullable=False, unique=True)
    name_short = Column(String(100), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    divisions = relationship("Division", back_populates="bureau", cascade="all, delete-orphan")
    users = relationship("User", back_populates="bureau")

