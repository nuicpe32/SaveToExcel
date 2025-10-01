from sqlalchemy import Column, Integer, String, DateTime, Text, Date, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class CriminalCase(Base):
    __tablename__ = "criminal_cases"

    id = Column(Integer, primary_key=True, index=True)

    # Case Identification
    case_number = Column(String, unique=True, index=True, nullable=False)
    case_id = Column(String, index=True, nullable=True)  # Allow NULL for cases without case_id

    # Case Status
    status = Column(String, default="ระหว่างสอบสวน")

    # Parties Involved
    complainant = Column(String)
    victim_name = Column(String)
    suspect = Column(String)

    # Case Details
    charge = Column(Text)
    case_type = Column(String)  # ประเภทคดี
    damage_amount = Column(String)
    case_scene = Column(Text)

    # Important Dates
    complaint_date = Column(Date)
    complaint_date_thai = Column(String)  # วันที่ในรูปแบบ พ.ศ.
    incident_date = Column(Date)
    incident_date_thai = Column(String)   # วันที่ในรูปแบบ พ.ศ.
    last_update_date = Column(Date)

    # Court and Prosecutor Information
    court_name = Column(String)
    prosecutor_name = Column(String)
    prosecutor_file_number = Column(String)

    # Officer Information
    officer_in_charge = Column(String)
    investigating_officer = Column(String)

    # Related Data Counts (for display purposes)
    bank_accounts_count = Column(Integer, default=0)
    bank_accounts_replied = Column(Integer, default=0)
    suspects_count = Column(Integer, default=0)
    suspects_replied = Column(Integer, default=0)

    # Case Age (calculated field)
    age_in_months = Column(Integer)
    is_over_six_months = Column(String)

    # Additional Information
    notes = Column(Text)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer)

    # Relationships
    bank_accounts = relationship("BankAccount", back_populates="criminal_case", cascade="all, delete-orphan")
    suspects = relationship("Suspect", back_populates="criminal_case", cascade="all, delete-orphan")
    post_arrests = relationship("PostArrest", back_populates="criminal_case", cascade="all, delete-orphan")