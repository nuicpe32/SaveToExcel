from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Charge(Base):
    __tablename__ = "charges"

    id = Column(Integer, primary_key=True, index=True)
    
    # Charge Information
    charge_name = Column(String(500), nullable=False, index=True)  # ชื่อข้อหา
    charge_description = Column(Text, nullable=False)  # ข้อหา (รายละเอียดเต็ม)
    related_laws = Column(Text, nullable=False)  # กฎหมายที่เกี่ยวข้อง
    penalty = Column(Text, nullable=False)  # อัตราโทษ
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
