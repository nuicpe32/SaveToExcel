from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Account reference
    account_type = Column(String(50), nullable=False, index=True)
    account_id = Column(Integer, nullable=False, index=True)
    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id", ondelete="CASCADE"), nullable=False, index=True)

    # Email details
    recipient_email = Column(String(255), nullable=False, index=True)
    subject = Column(String(500), nullable=False)
    document_type = Column(String(50), nullable=False)

    # Sending status
    status = Column(String(20), nullable=False, default='pending', index=True)
    sent_at = Column(DateTime(timezone=True))
    error_message = Column(Text)

    # Retry mechanism
    retry_count = Column(Integer, default=0)
    last_retry_at = Column(DateTime(timezone=True))

    # Tracking
    opened_at = Column(DateTime(timezone=True))
    opened_count = Column(Integer, default=0)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    sent_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    # PDF file reference
    pdf_filename = Column(String(255))
    pdf_size_bytes = Column(Integer)

    # Relationships
    criminal_case = relationship("CriminalCase", foreign_keys=[criminal_case_id])
    sender = relationship("User", foreign_keys=[sent_by])
