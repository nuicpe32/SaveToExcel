from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Court(Base):
    """Court master data model - ศาลทั้งหมดในประเทศไทย"""
    __tablename__ = "courts"

    id = Column(Integer, primary_key=True, index=True)
    court_name = Column(String(255), unique=True, nullable=False, index=True)
    court_type = Column(String(100), index=True)  # ศาลชั้นต้น, ศาลชำนัญพิเศษ, ศาลแขวง, ศาลจังหวัด, ศาลเยาวชนและครอบครัว
    region = Column(String(100), index=True)      # กรุงเทพฯ, ภาค 1-9
    province = Column(String(100))                # จังหวัด
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
