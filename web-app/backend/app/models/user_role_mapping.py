from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserRoleMapping(Base):
    __tablename__ = "user_roles_mapping"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="role_mappings")
    role = relationship("UserRole", back_populates="user_mappings")
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id', name='unique_user_role'),
    )
