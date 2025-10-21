from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class LineAccount(Base):
    __tablename__ = "line_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    line_user_id = Column(String(100), nullable=False, unique=True, index=True)
    line_display_name = Column(String(255))
    line_picture_url = Column(Text)
    line_status_message = Column(Text)

    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime(timezone=True))

    is_active = Column(Boolean, default=True, index=True)
    linked_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used_at = Column(DateTime(timezone=True))

    notify_new_case = Column(Boolean, default=True)
    notify_case_update = Column(Boolean, default=True)
    notify_summons_sent = Column(Boolean, default=True)
    notify_email_opened = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="line_account")
    notification_logs = relationship("LineNotificationLog", back_populates="line_account", cascade="all, delete-orphan")
