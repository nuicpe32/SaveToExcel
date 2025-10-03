"""
API endpoints สำหรับการแกะข้อมูลจากไฟล์ PDF
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.pdf_parser import pdf_parser

router = APIRouter()


@router.post("/parse-pdf-thor14")
async def parse_pdf_thor14(file: UploadFile = File(...)):
    """
    แกะข้อมูลจากไฟล์ PDF ทร.14
    
    Args:
        file: ไฟล์ PDF ที่อัปโหลด
        
    Returns:
        ข้อมูลที่แกะได้จาก PDF (ชื่อ, เลขบัตรประชาชน, ที่อยู่)
    """
    try:
        # ตรวจสอบว่าเป็นไฟล์ PDF หรือไม่
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="กรุณาอัปโหลดไฟล์ PDF เท่านั้น"
            )
        
        # ตรวจสอบขนาดไฟล์ (จำกัดที่ 10MB)
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=400,
                detail="ขนาดไฟล์ใหญ่เกินไป (จำกัดที่ 10MB)"
            )
        
        # สร้าง UploadFile object ใหม่เพื่อส่งไปยัง parser
        from io import BytesIO
        file.file = BytesIO(content)
        file.file.seek(0)
        
        # แกะข้อมูลจาก PDF
        extracted_data = await pdf_parser.parse_pdf(file)
        
        # ตรวจสอบว่ามีข้อมูลหรือไม่
        if not any(extracted_data.values()):
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": "ไม่สามารถแกะข้อมูลจากไฟล์ PDF ได้ กรุณาตรวจสอบรูปแบบไฟล์",
                    "data": extracted_data
                }
            )
        
        # ตรวจสอบความถูกต้องของที่อยู่
        address_valid = extracted_data.get('address_valid', True)
        
        # สร้างข้อความแจ้งเตือน
        message = "แกะข้อมูลจากไฟล์ PDF สำเร็จ"
        if not address_valid:
            message = "แกะข้อมูลจากไฟล์ PDF สำเร็จ แต่ระบบไม่สามารถแกะข้อมูลที่อยู่ของผู้ต้องหาจากไฟล์ได้ กรุณาระบุด้วยตนเอง"
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": message,
                "data": {
                    "name": extracted_data.get('name', ''),
                    "idCard": extracted_data.get('id_card', ''),
                    "address": extracted_data.get('address', ''),
                    "addressValid": address_valid
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in parse_pdf_thor14: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการประมวลผลไฟล์: {str(e)}"
        )
