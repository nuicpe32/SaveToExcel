from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.core import get_db
from app.models import User, BankAccount, Suspect, CriminalCase, Bank
from app.models.non_bank_account import NonBankAccount
from app.models.non_bank import NonBank
from app.services import DocumentGenerator
from app.services.bank_summons_generator import BankSummonsGenerator
from app.services.non_bank_summons_generator import NonBankSummonsGenerator
from app.services.suspect_summons_generator import suspect_summons_generator
from app.api.v1.auth import get_current_user
import os

router = APIRouter()

doc_generator = DocumentGenerator()
summons_generator = BankSummonsGenerator()
non_bank_summons_generator = NonBankSummonsGenerator()

@router.get("/bank-account/{bank_account_id}")
def generate_bank_account_document(
    bank_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bank_account = db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    data = {
        "document_number": bank_account.document_number,
        "bank_name": bank_account.bank_name,
        "account_number": bank_account.account_number,
        "account_name": bank_account.account_name,
        "branch": bank_account.branch,
        "request_date": bank_account.request_date
    }

    filepath = doc_generator.generate_bank_account_doc(data)

    return FileResponse(
        path=filepath,
        filename=os.path.basename(filepath),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@router.get("/bank-summons/{bank_account_id}", response_class=HTMLResponse)
def generate_bank_summons_html(
    bank_account_id: int,
    freeze_account: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างหมายเรียกธนาคาร (HTML) สำหรับบัญชีธนาคารรายการเดียว
    
    Args:
        freeze_account: True = อายัดบัญชี, False = ไม่อายัดบัญชี (default)
    """
    
    # ดึงข้อมูลบัญชีธนาคาร
    bank_account = db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    
    # ดึงข้อมูลคดี
    criminal_case = db.query(CriminalCase).filter(
        CriminalCase.id == bank_account.criminal_case_id
    ).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # แปลงข้อมูลเป็น dict
    bank_data = {
        'id': bank_account.id,
        'document_number': bank_account.document_number,
        'document_date': bank_account.document_date,
        'bank_name': bank_account.bank_name,
        'account_number': bank_account.account_number,
        'account_name': bank_account.account_name,
        'time_period': bank_account.time_period,
    }
    
    # ใช้ complainant เป็นฟิลด์หลักสำหรับผู้เสียหาย/ผู้กล่าวหา
    complainant_name = criminal_case.complainant or 'ผู้เสียหาย'
    
    case_data = {
        'case_id': criminal_case.case_id,
        'case_number': criminal_case.case_number,
        'victim_name': complainant_name,  # ส่งเป็น victim_name เพื่อ backward compatibility กับ template
        'complainant': complainant_name,
    }
    
    # สร้าง HTML (ส่ง freeze_account parameter)
    html_content = summons_generator.generate_bank_letter_html(bank_data, case_data, freeze_account)
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")

@router.get("/bank-envelope/{bank_account_id}", response_class=HTMLResponse)
def generate_bank_envelope_html(
    bank_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างซองหมายเรียกธนาคาร (HTML)"""
    
    # ดึงข้อมูลบัญชีธนาคาร
    bank_account = db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    
    # แปลงข้อมูลเป็น dict
    bank_data = {
        'document_number': bank_account.document_number,
        'bank_name': bank_account.bank_name,
    }
    
    # ดึงข้อมูลที่อยู่ธนาคาร (ถ้ามี bank_id)
    bank_address = None
    
    if bank_account.bank_id:
        bank = db.query(Bank).filter(Bank.id == bank_account.bank_id).first()
        if bank:
            bank_address = {
                'bank_address': bank.bank_address,
                'soi': bank.soi,
                'moo': bank.moo,
                'road': bank.road,
                'sub_district': bank.sub_district,
                'district': bank.district,
                'province': bank.province,
                'postal_code': bank.postal_code,
            }
    else:
        # Fallback: ลอง lookup จาก bank_name (กรณี bank_id ไม่มีค่า)
        if bank_account.bank_name:
            # ลองหาแบบตรงทั้งหมดก่อน
            bank = db.query(Bank).filter(Bank.bank_name == bank_account.bank_name).first()
            
            # ถ้าไม่เจอ ลองตัดคำว่า "ธนาคาร" ออก
            if not bank:
                bank_name_without_prefix = bank_account.bank_name.replace('ธนาคาร', '').strip()
                bank = db.query(Bank).filter(Bank.bank_name == bank_name_without_prefix).first()
            
            # ถ้ายังไม่เจอ ลองหาแบบ LIKE
            if not bank:
                bank_name_search = f"%{bank_account.bank_name.replace('ธนาคาร', '').strip()}%"
                bank = db.query(Bank).filter(Bank.bank_name.like(bank_name_search)).first()
            
            if bank:
                bank_address = {
                    'bank_address': bank.bank_address,
                    'soi': bank.soi,
                    'moo': bank.moo,
                    'road': bank.road,
                    'sub_district': bank.sub_district,
                    'district': bank.district,
                    'province': bank.province,
                    'postal_code': bank.postal_code,
                }
    
    # สร้าง HTML
    html_content = summons_generator.generate_envelope_html(bank_data, bank_address)
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")

@router.get("/suspect-summons/{suspect_id}", response_class=HTMLResponse)
def generate_suspect_summons_html(
    suspect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างหมายเรียกผู้ต้องหา (HTML) สำหรับผู้ต้องหารายการเดียว"""
    
    # ดึงข้อมูลผู้ต้องหา
    suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    if not suspect:
        raise HTTPException(status_code=404, detail="Suspect not found")
    
    # ดึงข้อมูลคดี
    criminal_case = db.query(CriminalCase).filter(
        CriminalCase.id == suspect.criminal_case_id
    ).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # แปลงข้อมูลเป็น dict
    suspect_data = {
        'id': suspect.id,
        'document_number': suspect.document_number,
        'document_date': suspect.document_date,
        'suspect_name': suspect.suspect_name,
        'suspect_id_card': suspect.suspect_id_card,
        'suspect_address': suspect.suspect_address,
        'police_station': suspect.police_station,
        'police_province': suspect.police_province,
        'police_address': suspect.police_address,
        'appointment_date': suspect.appointment_date,
        'appointment_date_thai': suspect.appointment_date_thai,
        'reply_status': suspect.reply_status,
    }
    
    # ใช้ complainant เป็นฟิลด์หลักสำหรับผู้เสียหาย/ผู้กล่าวหา
    complainant_name = criminal_case.complainant or 'ผู้เสียหาย'
    
    case_data = {
        'case_id': criminal_case.case_id,
        'case_number': criminal_case.case_number,
        'victim_name': complainant_name,  # ส่งเป็น victim_name เพื่อ backward compatibility กับ template
        'complainant': complainant_name,
        'case_type': criminal_case.case_type,
        'damage_amount': criminal_case.damage_amount,
        'court_name': criminal_case.court_name,
    }
    
    # สร้าง HTML
    html_content = suspect_summons_generator.generate_suspect_letter_html(suspect_data, case_data)
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")

@router.get("/suspect-envelope/{suspect_id}", response_class=HTMLResponse)
def generate_suspect_envelope_html(
    suspect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างซองหมายเรียกผู้ต้องหา (HTML)"""
    
    # ดึงข้อมูลผู้ต้องหา
    suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    if not suspect:
        raise HTTPException(status_code=404, detail="Suspect not found")
    
    # แปลงข้อมูลเป็น dict
    suspect_data = {
        'id': suspect.id,
        'document_number': suspect.document_number,
        'document_date': suspect.document_date,
        'suspect_name': suspect.suspect_name,
        'suspect_id_card': suspect.suspect_id_card,
        'police_station': suspect.police_station,
        'police_province': suspect.police_province,
        'police_address': suspect.police_address,
    }
    
    # สร้าง HTML
    html_content = suspect_summons_generator.generate_suspect_envelope_html(suspect_data)
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")

# ==================== Non-Bank Summons Endpoints ====================

@router.get("/non-bank-summons/{non_bank_account_id}", response_class=HTMLResponse)
def generate_non_bank_summons_html(
    non_bank_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างหมายเรียกผู้ให้บริการ Non-Bank (HTML)"""
    
    # ดึงข้อมูลบัญชี Non-Bank
    non_bank_account = db.query(NonBankAccount).filter(
        NonBankAccount.id == non_bank_account_id
    ).first()
    if not non_bank_account:
        raise HTTPException(status_code=404, detail="Non-bank account not found")
    
    # ดึงข้อมูลคดี
    criminal_case = db.query(CriminalCase).filter(
        CriminalCase.id == non_bank_account.criminal_case_id
    ).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # แปลงข้อมูลเป็น dict
    non_bank_data = {
        'document_number': non_bank_account.document_number,
        'document_date': non_bank_account.document_date,
        'document_date_thai': non_bank_account.document_date_thai,
        'provider_name': non_bank_account.provider_name,
        'account_number': non_bank_account.account_number,
        'account_name': non_bank_account.account_name,
        'time_period': non_bank_account.time_period,
        'delivery_date': non_bank_account.delivery_date,
        'is_frozen': non_bank_account.is_frozen,
    }
    
    case_data = {
        'case_id': criminal_case.case_id,
        'case_number': criminal_case.case_number,
        'complainant': criminal_case.complainant,
        'case_type': criminal_case.case_type,
        'damage_amount': criminal_case.damage_amount,
    }
    
    # สร้าง HTML (ใช้ฟังก์ชันเดียวกับ bank แต่จะส่งข้อมูล non_bank)
    freeze_account = non_bank_account.is_frozen
    html_content = non_bank_summons_generator.generate_bank_letter_html(non_bank_data, case_data, freeze_account)
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")

@router.get("/non-bank-envelope/{non_bank_account_id}", response_class=HTMLResponse)
def generate_non_bank_envelope_html(
    non_bank_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างซองหมายเรียกผู้ให้บริการ Non-Bank (HTML)"""
    
    # ดึงข้อมูลบัญชี Non-Bank
    non_bank_account = db.query(NonBankAccount).filter(
        NonBankAccount.id == non_bank_account_id
    ).first()
    if not non_bank_account:
        raise HTTPException(status_code=404, detail="Non-bank account not found")
    
    # แปลงข้อมูลเป็น dict
    non_bank_data = {
        'document_number': non_bank_account.document_number,
        'provider_name': non_bank_account.provider_name,
    }
    
    # ดึงข้อมูลที่อยู่ผู้ให้บริการ (ถ้ามี non_bank_id)
    non_bank_address = None
    
    if non_bank_account.non_bank_id:
        non_bank = db.query(NonBank).filter(NonBank.id == non_bank_account.non_bank_id).first()
        if non_bank:
            non_bank_address = {
                'company_address': non_bank.company_address,
                'soi': non_bank.soi,
                'moo': non_bank.moo,
                'road': non_bank.road,
                'sub_district': non_bank.sub_district,
                'district': non_bank.district,
                'province': non_bank.province,
                'postal_code': non_bank.postal_code,
            }
    else:
        # Fallback: ลอง lookup จาก provider_name
        if non_bank_account.provider_name:
            # ลองหาแบบตรงทั้งหมดก่อน
            non_bank = db.query(NonBank).filter(
                NonBank.company_name == non_bank_account.provider_name
            ).first()
            
            # ถ้าไม่เจอ ลองหาจาก company_name_short
            if not non_bank:
                non_bank = db.query(NonBank).filter(
                    NonBank.company_name_short == non_bank_account.provider_name
                ).first()
            
            # ถ้ายังไม่เจอ ลองหาแบบ LIKE
            if not non_bank:
                search_pattern = f"%{non_bank_account.provider_name}%"
                non_bank = db.query(NonBank).filter(
                    NonBank.company_name.like(search_pattern)
                ).first()
            
            if non_bank:
                non_bank_address = {
                    'company_address': non_bank.company_address,
                    'soi': non_bank.soi,
                    'moo': non_bank.moo,
                    'road': non_bank.road,
                    'sub_district': non_bank.sub_district,
                    'district': non_bank.district,
                    'province': non_bank.province,
                    'postal_code': non_bank.postal_code,
                }
    
    # สร้าง HTML
    html_content = non_bank_summons_generator.generate_envelope_html(non_bank_data, non_bank_address)
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")