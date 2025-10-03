from sqlalchemy import Column, Integer, String, DateTime, Text, Date, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class PostArrest(Base):
    __tablename__ = "post_arrests"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key to Criminal Case
    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id"), nullable=True, index=True)

    # Case Information
    case_number = Column(String, index=True)       # คดีอาญาที่
    accuser_name = Column(String, index=True)      # ผู้กล่าวหา

    # Suspect Information
    suspect_name = Column(String, nullable=False, index=True)  # ชื่อผู้ต้องหา
    suspect_age = Column(Integer)
    suspect_nationality = Column(String)
    suspect_address = Column(Text)
    suspect_id_card = Column(String, index=True)   # เลข ปชช
    suspect_occupation = Column(String)

    # Court Information
    warrant_court = Column(String, index=True)
    warrant_number = Column(String, index=True)    # เลขหมาย
    warrant_petition_date = Column(Date)           # วันที่ออกหมายจับ
    warrant_issue_date = Column(Date)              # ลงหมาย

    # Arrest Information
    arrest_date = Column(Date)
    arrest_time = Column(String)
    arresting_officer = Column(String)
    arresting_unit = Column(String)
    arrest_location = Column(String)

    # Document Information
    warrant_revocation_doc = Column(String)
    custody_transfer_doc = Column(String)

    # Case Details
    charges = Column(Text)
    law_sections = Column(Text)
    penalties = Column(Text)
    circumstances = Column(Text)
    evidence_items = Column(Text)

    # Detention Information
    detention_period_1 = Column(String)
    detention_period_2 = Column(String)

    # Prosecutor Information
    prosecutor_transfer_date = Column(Date)
    prosecutor_doc_number = Column(String)
    prosecutor_name = Column(String)

    # Court Proceedings
    case_submission_date = Column(Date)
    detention_request_date = Column(Date)
    detention_request_doc = Column(String)
    court_name = Column(String)
    court_custody_transfer_date = Column(Date)
    court_custody_location = Column(String)

    # Interrogation
    interrogation_completed = Column(Boolean)
    interrogation_date = Column(Date)

    # Bail Information
    bail_requested = Column(Boolean)
    bail_amount = Column(String)
    bail_status = Column(String)

    # Status and Notes
    status = Column(String)
    notes = Column(Text)

    # Crime Scene and Damage
    crime_scene = Column(Text)
    damage_amount = Column(String)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer)

    # Relationships
    criminal_case = relationship("CriminalCase", back_populates="post_arrests")
