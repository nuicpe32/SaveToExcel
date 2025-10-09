from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class PoliceRank(Base):
    __tablename__ = "police_ranks"

    id = Column(Integer, primary_key=True, index=True)
    rank_full = Column(String(100), nullable=False, index=True)
    rank_short = Column(String(20), nullable=False, index=True)
    rank_english = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    users = relationship("User", back_populates="rank")
