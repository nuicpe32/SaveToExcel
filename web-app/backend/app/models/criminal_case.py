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

    # Case Details
    case_type = Column(String)  # ประเภทคดี
    damage_amount = Column(String)

    # Important Dates
    complaint_date = Column(Date)
    incident_date = Column(Date)
    last_update_date = Column(Date)

    # Court Information
    court_name = Column(String)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # Relationships
    bank_accounts = relationship("BankAccount", back_populates="criminal_case", cascade="all, delete-orphan")
    non_bank_accounts = relationship("NonBankAccount", back_populates="criminal_case", cascade="all, delete-orphan")
    telco_mobile_accounts = relationship("TelcoMobileAccount", back_populates="criminal_case", cascade="all, delete-orphan")
    telco_internet_accounts = relationship("TelcoInternetAccount", back_populates="criminal_case", cascade="all, delete-orphan")
    suspects = relationship("Suspect", back_populates="criminal_case", cascade="all, delete-orphan")
    post_arrests = relationship("PostArrest", back_populates="criminal_case", cascade="all, delete-orphan")
    cfr_records = relationship("CFR", back_populates="criminal_case", cascade="all, delete-orphan")
    owner = relationship("User", foreign_keys=[owner_id], overlaps="owned_criminal_cases")