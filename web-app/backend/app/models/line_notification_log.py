from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class LineNotificationLog(Base):
    __tablename__ = "line_notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    line_account_id = Column(Integer, ForeignKey("line_accounts.id", ondelete="CASCADE"), nullable=False)

    notification_type = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)

    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id", ondelete="SET NULL"))

    status = Column(String(20), default="pending", index=True)
    error_message = Column(Text)
    sent_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    line_account = relationship("LineAccount", back_populates="notification_logs")
    criminal_case = relationship("CriminalCase")
