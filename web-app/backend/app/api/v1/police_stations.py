"""
API endpoints สำหรับค้นหาสถานีตำรวจ
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services.police_station_service import police_station_service

router = APIRouter()


class PoliceStationSearchRequest(BaseModel):
    address: str


@router.post("/search")
async def search_police_stations(request: PoliceStationSearchRequest):
    """
    ค้นหาสถานีตำรวจจากที่อยู่
    
    Args:
        request: ข้อมูลที่อยู่สำหรับค้นหา
        
    Returns:
        รายการสถานีตำรวจที่พบ
    """
    try:
        if not request.address or not request.address.strip():
            raise HTTPException(
                status_code=400,
                detail="กรุณาระบุที่อยู่สำหรับค้นหา"
            )
        
        # ค้นหาสถานีตำรวจ
        stations = await police_station_service.search_police_stations(request.address.strip())
        
        if not stations:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": "ไม่พบสถานีตำรวจในพื้นที่นี้",
                    "stations": []
                }
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": f"พบสถานีตำรวจ {len(stations)} แห่ง",
                "stations": stations
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in search_police_stations endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการค้นหาสถานีตำรวจ: {str(e)}"
        )
