from sqlalchemy import Column, Integer, String, DateTime, Text, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class PostArrest(Base):
    __tablename__ = "post_arrests"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key to Criminal Case
    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id"), nullable=False, index=True)

    # Case Information
    case_criminal_no = Column(String, index=True)  # คดีอาญาที่
    accuser = Column(String, index=True)           # ผู้กล่าวหา

    # Suspect Information
    suspect_name = Column(String, nullable=False, index=True)  # ชื่อผู้ต้องหา
    age = Column(Integer)
    nationality = Column(String)
    address = Column(Text)
    id_card = Column(String, index=True)           # เลข ปชช
    occupation = Column(String)

    # Court Information
    court = Column(String, index=True)
    warrant_no = Column(String, index=True)        # เลขหมาย
    warrant_date = Column(Date)                    # วันที่ออกหมายจับ
    warrant_issued = Column(String)                # ลงหมาย

    # Petition Information
    petition_day = Column(Integer)
    petition_month = Column(String)
    petition_year = Column(Integer)

    # Arrest Information
    arrest_date = Column(Date, index=True)         # วันที่จับ
    arrest_time = Column(String)                   # เวลาจับ
    arrest_location = Column(Text)                 # สถานที่จับ
    arresting_officer = Column(String)             # ผู้นำจับ

    # Witnesses
    witness_1 = Column(String)
    witness_2 = Column(String)

    # Case Details
    charges = Column(Text)                         # ข้อหา
    crime_scene = Column(Text)                     # ที่เกิดเหตุในคดี
    damage_amount = Column(String)                 # ความเสียหาย
    facts = Column(Text)                           # ข้อเท็จจริง

    # Transfer Information
    transfer_date = Column(Date)                   # วันที่ส่งผู้ต้องหา
    transfer_time = Column(String)                 # เวลาส่งผู้ต้องหา
    transfer_agency = Column(String)               # หน่วยงานที่ส่ง
    receiver = Column(String)                      # ผู้รับส่ง

    # Court Order Information
    court_order = Column(String)                   # คำสั่งศาล
    order_no = Column(String)                      # เลขที่คำสั่ง
    order_date = Column(Date)                      # วันที่คำสั่ง
    case_result = Column(String)                   # ผลการดำเนินคดี

    # Court Decision
    charges_laid = Column(Text)                    # ข้อหาที่ตั้ง
    verdict = Column(Text)                         # ผลคำพิพากษา
    verdict_date = Column(Date)                    # วันที่พิพากษา
    verdict_notes = Column(Text)                   # หมายเหตุการพิพากษา

    # Status
    case_status = Column(String, index=True)       # สถานะคดี

    # Document Information
    document_creator = Column(String)              # ผู้จัดทำเอกสาร
    document_date = Column(Date)                   # วันที่จัดทำเอกสาร
    additional_notes = Column(Text)                # หมายเหตุเพิ่มเติม

    # Additional Information
    notes = Column(Text)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer)

    # Relationships
    criminal_case = relationship("CriminalCase", back_populates="post_arrests")