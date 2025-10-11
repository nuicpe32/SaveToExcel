from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Supervision(Base):
    """Model สำหรับหน่วยงานระดับกองกำกับการ (กก.)"""
    __tablename__ = "supervisions"

    id = Column(Integer, primary_key=True, index=True)
    division_id = Column(Integer, ForeignKey("divisions.id", ondelete="CASCADE"), nullable=False, index=True)
    name_full = Column(String(255), nullable=False)
    name_short = Column(String(100), nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    division = relationship("Division", back_populates="supervisions")
    users = relationship("User", back_populates="supervision")

