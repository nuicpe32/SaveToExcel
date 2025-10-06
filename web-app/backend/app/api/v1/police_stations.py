"""
API endpoints สำหรับค้นหาสถานีตำรวจ
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.police_station_service import PoliceStationService
from app.schemas.police_station import PoliceStationSearchRequest, PoliceStationSearchResponse

router = APIRouter()


@router.post("/search", response_model=PoliceStationSearchResponse)
async def search_police_stations(
    request: PoliceStationSearchRequest,
    db: Session = Depends(get_db)
):
    """
    ค้นหาสถานีตำรวจจากที่อยู่
    
    Args:
        request: ข้อมูลที่อยู่สำหรับค้นหา
        db: Database session
        
    Returns:
        รายการสถานีตำรวจที่พบ
    """
    try:
        if not request.address or not request.address.strip():
            raise HTTPException(
                status_code=400,
                detail="กรุณาระบุที่อยู่สำหรับค้นหา"
            )
        
        # สร้าง service instance
        service = PoliceStationService(db)
        
        # ค้นหาสถานีตำรวจ
        result = service.search_police_stations(request.address.strip())
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in search_police_stations endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการค้นหาสถานีตำรวจ: {str(e)}"
        )


@router.get("/provinces")
async def get_provinces(db: Session = Depends(get_db)):
    """Get all provinces with police stations"""
    try:
        service = PoliceStationService(db)
        stations = service.get_all_stations(limit=1000)
        
        provinces = list(set([station.province for station in stations if station.province]))
        provinces.sort()
        
        return {
            "success": True,
            "provinces": provinces
        }
        
    except Exception as e:
        print(f"Error in get_provinces endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการดึงข้อมูลจังหวัด: {str(e)}"
        )


@router.get("/stations/{province}")
async def get_stations_by_province(
    province: str,
    db: Session = Depends(get_db)
):
    """Get all police stations in a specific province"""
    try:
        service = PoliceStationService(db)
        stations = service.get_stations_by_province(province)
        
        return {
            "success": True,
            "province": province,
            "stations": stations
        }
        
    except Exception as e:
        print(f"Error in get_stations_by_province endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการดึงข้อมูลสถานีตำรวจ: {str(e)}"
        )
