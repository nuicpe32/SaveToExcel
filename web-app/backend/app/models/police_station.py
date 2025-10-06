from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class PoliceStation(Base):
    __tablename__ = "police_stations_master"

    id = Column(Integer, primary_key=True, index=True)
    station_name = Column(String(255), nullable=False, index=True)
    station_code = Column(String(50))
    province = Column(String(100), nullable=False, index=True)
    district = Column(String(100))
    subdistrict = Column(String(100))
    address = Column(Text)
    postal_code = Column(String(10))
    phone = Column(String(50))
    subdistricts_covered = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
