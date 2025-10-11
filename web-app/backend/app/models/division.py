from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Division(Base):
    """Model สำหรับหน่วยงานระดับกองบังคับการ (บก.)"""
    __tablename__ = "divisions"

    id = Column(Integer, primary_key=True, index=True)
    bureau_id = Column(Integer, ForeignKey("bureaus.id", ondelete="CASCADE"), nullable=False, index=True)
    name_full = Column(String(255), nullable=False)
    name_short = Column(String(100), nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    bureau = relationship("Bureau", back_populates="divisions")
    supervisions = relationship("Supervision", back_populates="division", cascade="all, delete-orphan")
    users = relationship("User", back_populates="division")

