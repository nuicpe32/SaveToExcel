from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Police information
    rank_id = Column(Integer, ForeignKey("police_ranks.id"), nullable=True)
    full_name = Column(String, nullable=False)
    position = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    line_id = Column(String, nullable=True)
    signature_path = Column(String(500), nullable=True, comment="Path to user signature image file (PNG format)")
    
    # Organization (Required)
    bureau_id = Column(Integer, ForeignKey("bureaus.id"), nullable=False, index=True)
    division_id = Column(Integer, ForeignKey("divisions.id"), nullable=False, index=True)
    supervision_id = Column(Integer, ForeignKey("supervisions.id"), nullable=False, index=True)
    
    # Role and permissions
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    
    # Account status
    is_active = Column(Boolean, default=False)  # Default to False, requires admin approval
    is_approved = Column(Boolean, default=False)  # Admin approval status
    
    # Login security
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    approved_at = Column(DateTime, nullable=True)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    rank = relationship("PoliceRank", back_populates="users")
    role = relationship("UserRole", back_populates="users")
    role_mappings = relationship("UserRoleMapping", back_populates="user", cascade="all, delete-orphan")
    approver = relationship("User", remote_side=[id], back_populates="approved_users")
    approved_users = relationship("User", back_populates="approver")
    owned_criminal_cases = relationship("CriminalCase", foreign_keys="CriminalCase.owner_id", overlaps="owner")
    
    # Organization Relationships
    bureau = relationship("Bureau", back_populates="users")
    division = relationship("Division", back_populates="users")
    supervision = relationship("Supervision", back_populates="users")