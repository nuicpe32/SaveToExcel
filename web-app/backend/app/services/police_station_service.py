#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service for police station search and management
"""

import re
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.police_station import PoliceStation
from app.schemas.police_station import PoliceStationSearchResponse, PoliceStationResponse

class PoliceStationService:
    """Service for police station operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def extract_address_components(self, address: str) -> Dict[str, str]:
        """
        Extract province, district, and subdistrict from address
        
        Args:
            address: Full address string
            
        Returns:
            Dict with province, district, subdistrict
        """
        if not address:
            return {"province": "", "district": "", "subdistrict": ""}
        
        # Clean address
        address = address.strip()
        
        # Extract province (จ. or จังหวัด)
        province_match = re.search(r'(?:จ\.|จังหวัด)\s*([^\s,]+)', address)
        province = province_match.group(1) if province_match else ""
        
        # Extract district (อ. or อำเภอ)
        district_match = re.search(r'(?:อ\.|อำเภอ)\s*([^\s,]+)', address)
        district = district_match.group(1) if district_match else ""
        
        # Extract subdistrict (ต. or ตำบล)
        subdistrict_match = re.search(r'(?:ต\.|ตำบล)\s*([^\s,]+)', address)
        subdistrict = subdistrict_match.group(1) if subdistrict_match else ""
        
        return {
            "province": province,
            "district": district,
            "subdistrict": subdistrict
        }
    
    def search_police_stations(self, address: str) -> PoliceStationSearchResponse:
        """
        Search police stations based on suspect address
        
        Args:
            address: Suspect's address
            
        Returns:
            PoliceStationSearchResponse with matches
        """
        # Extract address components
        components = self.extract_address_components(address)
        province = components["province"]
        district = components["district"]
        subdistrict = components["subdistrict"]
        
        result = PoliceStationSearchResponse()
        
        if not province:
            return result
        
        # 1. Search for exact subdistrict match
        if subdistrict:
            exact_match = self._find_exact_subdistrict_match(province, subdistrict)
            if exact_match:
                result.exact_match = PoliceStationResponse.from_orm(exact_match)
                # Check if exact match has incomplete address
                if self._has_incomplete_address(exact_match.address):
                    result.has_incomplete_address = True
                    result.warning_message = "ข้อมูลสถานีตำรวจไม่สมบูรณ์ กรุณาตรวจสอบโดยตรงกับสถานีตำรวจอีกครั้ง"
                return result
        
        # 2. Search for district matches
        if district:
            district_matches = self._find_district_matches(province, district)
            result.district_matches = [PoliceStationResponse.from_orm(station) for station in district_matches]
            # Check if any district match has incomplete address
            if any(self._has_incomplete_address(station.address) for station in district_matches):
                result.has_incomplete_address = True
                result.warning_message = "ข้อมูลสถานีตำรวจไม่สมบูรณ์ กรุณาตรวจสอบโดยตรงกับสถานีตำรวจอีกครั้ง"
        
        # 3. Search for province matches (fallback)
        province_matches = self._find_province_matches(province)
        result.province_matches = [PoliceStationResponse.from_orm(station) for station in province_matches]
        # Check if any province match has incomplete address
        if any(self._has_incomplete_address(station.address) for station in province_matches):
            result.has_incomplete_address = True
            result.warning_message = "ข้อมูลสถานีตำรวจไม่สมบูรณ์ กรุณาตรวจสอบโดยตรงกับสถานีตำรวจอีกครั้ง"
        
        # 4. If no matches found, create a fallback response
        if not result.exact_match and not result.district_matches and not result.province_matches:
            result = self._create_fallback_response(province, district, subdistrict)
        
        return result
    
    def _create_fallback_response(self, province: str, district: str, subdistrict: str) -> PoliceStationSearchResponse:
        """Create fallback response when no police station is found in database"""
        
        # Create a mock police station for the area
        fallback_station = PoliceStationResponse(
            id=999999,  # Special ID for fallback
            station_name=f"สถานีตำรวจในพื้นที่ {province}",
            station_code="",
            province=province,
            district=district or "",
            subdistrict=subdistrict or "",
            address=f"พื้นที่ {subdistrict or district or province} จังหวัด{province}",
            postal_code="",
            phone="",
            subdistricts_covered=f"{subdistrict or district or province}",
            created_at=None,
            updated_at=None
        )
        
        result = PoliceStationSearchResponse()
        result.province_matches = [fallback_station]
        
        return result
    
    def _find_exact_subdistrict_match(self, province: str, subdistrict: str) -> Optional[PoliceStation]:
        """Find police station that covers the exact subdistrict"""
        
        # Search for stations in the same province
        stations = self.db.query(PoliceStation).filter(
            PoliceStation.province.ilike(f"%{province}%")
        ).all()
        
        for station in stations:
            if station.subdistricts_covered:
                # Check if subdistrict is in the covered areas
                covered_areas = station.subdistricts_covered.split(',')
                for area in covered_areas:
                    area = area.strip()
                    if subdistrict in area or area in subdistrict:
                        return station
        
        return None
    
    def _find_district_matches(self, province: str, district: str) -> List[PoliceStation]:
        """Find police stations in the same district"""
        
        # Search for stations in the same province and district
        stations = self.db.query(PoliceStation).filter(
            and_(
                PoliceStation.province.ilike(f"%{province}%"),
                PoliceStation.district.ilike(f"%{district}%")
            )
        ).all()
        
        # If no district match, search by province only
        if not stations:
            stations = self.db.query(PoliceStation).filter(
                PoliceStation.province.ilike(f"%{province}%")
            ).limit(10).all()
            
            return stations
            
    def _find_province_matches(self, province: str) -> List[PoliceStation]:
        """Find police stations in the same province"""
        
        # Try exact match first
        stations = self.db.query(PoliceStation).filter(
            PoliceStation.province == province
        ).limit(20).all()
        
        # If no exact match, try partial match
        if not stations:
            stations = self.db.query(PoliceStation).filter(
                PoliceStation.province.ilike(f"%{province}%")
            ).limit(20).all()
                
        return stations
            
    def get_all_stations(self, skip: int = 0, limit: int = 100) -> List[PoliceStation]:
        """Get all police stations with pagination"""
        return self.db.query(PoliceStation).offset(skip).limit(limit).all()
    
    def get_stations_by_province(self, province: str) -> List[PoliceStation]:
        """Get all police stations in a specific province"""
        return self.db.query(PoliceStation).filter(
            PoliceStation.province.ilike(f"%{province}%")
        ).all()
    
    def get_station_by_id(self, station_id: int) -> Optional[PoliceStation]:
        """Get police station by ID"""
        return self.db.query(PoliceStation).filter(PoliceStation.id == station_id).first()
    
    def _has_incomplete_address(self, address: Optional[str]) -> bool:
        """
        Check if police station address is incomplete (no house number)
        
        Args:
            address: Police station address
            
        Returns:
            True if address is incomplete (no house number), False otherwise
        """
        if not address or address.strip() == "":
            return True
        
        # Check if address starts with a number (house number)
        # This regex checks for patterns like "123", "123/45", "123-45", etc.
        if re.match(r'^[0-9]+', address.strip()):
            return False
        
        # If address doesn't start with a number, it's considered incomplete
        return True