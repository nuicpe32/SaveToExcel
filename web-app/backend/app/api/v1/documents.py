from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.core import get_db
from app.models import User, BankAccount, Suspect, CriminalCase, Bank
from app.services import DocumentGenerator
from app.services.bank_summons_generator import BankSummonsGenerator
from app.services.suspect_summons_generator import suspect_summons_generator
from app.api.v1.auth import get_current_user
import os

router = APIRouter()

doc_generator = DocumentGenerator()
summons_generator = BankSummonsGenerator()

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างหมายเรียกธนาคาร (HTML) สำหรับบัญชีธนาคารรายการเดียว"""
    
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
        'document_date_thai': bank_account.document_date_thai,
        'bank_name': bank_account.bank_name,
        'account_number': bank_account.account_number,
        'account_name': bank_account.account_name,
        'time_period': bank_account.time_period,
    }
    
    case_data = {
        'case_id': criminal_case.case_id,
        'case_number': criminal_case.case_number,
        'victim_name': criminal_case.victim_name or criminal_case.complainant,
        'complainant': criminal_case.complainant,
    }
    
    # สร้าง HTML
    html_content = summons_generator.generate_bank_letter_html(bank_data, case_data)
    
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
        'document_date_thai': suspect.document_date_thai,
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
    
    case_data = {
        'case_id': criminal_case.case_id,
        'case_number': criminal_case.case_number,
        'victim_name': criminal_case.victim_name or criminal_case.complainant,
        'complainant': criminal_case.complainant,
        'case_type': criminal_case.case_type,
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
        'suspect_name': suspect.suspect_name,
        'suspect_id_card': suspect.suspect_id_card,
        'police_station': suspect.police_station,
        'police_province': suspect.police_province,
        'police_address': suspect.police_address,
    }
    
    # สร้าง HTML
    html_content = suspect_summons_generator.generate_suspect_envelope_html(suspect_data)
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")