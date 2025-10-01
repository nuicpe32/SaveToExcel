from sqlalchemy import Column, Integer, String, DateTime, Text, Date, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Suspect(Base):
    __tablename__ = "suspects"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key to Criminal Case (REQUIRED)
    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id", ondelete="CASCADE"), nullable=False, index=True)

    # Document Information
    document_number = Column(String, index=True)
    document_date = Column(Date)
    document_date_thai = Column(String)  # วันที่ในรูปแบบไทย เช่น "26 ส.ค. 68"

    # Suspect Information
    suspect_name = Column(String, nullable=False, index=True)
    suspect_id_card = Column(String, index=True)
    suspect_address = Column(Text)

    # Police Station Information
    police_station = Column(String, index=True)
    police_province = Column(String, index=True)
    police_address = Column(Text)

    # Case Type
    case_type = Column(String, index=True)  # ประเภทคดี

    # Appointment Information
    appointment_date = Column(Date, index=True)
    appointment_date_thai = Column(String)

    # Reply Status
    reply_status = Column(Boolean, default=False, index=True)

    # Status
    status = Column(String, default="pending", index=True)
    notes = Column(Text)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer)

    # Relationships
    criminal_case = relationship("CriminalCase", back_populates="suspects")