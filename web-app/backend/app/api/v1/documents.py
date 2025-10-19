from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.core import get_db
from app.models import User, BankAccount, Suspect, CriminalCase, Bank, TelcoMobileAccount, TelcoMobile, TelcoInternetAccount, TelcoInternet
from app.models.non_bank_account import NonBankAccount
from app.models.non_bank import NonBank
from app.services import DocumentGenerator
from app.services.bank_summons_generator import BankSummonsGenerator
from app.services.non_bank_summons_generator import NonBankSummonsGenerator
from app.services.payment_gateway_summons_generator import PaymentGatewaySummonsGenerator
from app.services.telco_mobile_summons_generator import TelcoMobileSummonsGenerator
from app.services.telco_internet_summons_generator import TelcoInternetSummonsGenerator
from app.services.suspect_summons_generator import suspect_summons_generator
from app.services.case_report_generator import CaseReportGenerator
from app.api.v1.auth import get_current_user
import os

router = APIRouter()

doc_generator = DocumentGenerator()
summons_generator = BankSummonsGenerator()
non_bank_summons_generator = NonBankSummonsGenerator()
payment_gateway_summons_generator = PaymentGatewaySummonsGenerator()
telco_mobile_summons_generator = TelcoMobileSummonsGenerator()
telco_internet_summons_generator = TelcoInternetSummonsGenerator()
case_report_generator = CaseReportGenerator()

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
    freeze_account: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างหมายเรียกผู้ให้บริการ Non-Bank (HTML)"""
    from app.models.non_bank_transaction import NonBankTransaction
    from app.models.bank import Bank
    
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

    # ดึงข้อมูลผู้ให้บริการจาก non_banks table
    provider_name = ''
    if non_bank_account.non_bank_id:
        non_bank = db.query(NonBank).filter(NonBank.id == non_bank_account.non_bank_id).first()
        if non_bank:
            provider_name = non_bank.company_name
    
    # ดึงรายการโอนที่เกี่ยวข้อง (ถ้ามี)
    transactions = db.query(NonBankTransaction).filter(
        NonBankTransaction.non_bank_account_id == non_bank_account_id
    ).order_by(NonBankTransaction.transfer_date).all()
    
    # แปลงรายการโอนเป็น list of dicts
    transaction_list = []
    if transactions:
        for t in transactions:
            # ดึงชื่อธนาคารต้นทาง
            source_bank_name = ''
            if t.source_bank_id:
                bank = db.query(Bank).filter(Bank.id == t.source_bank_id).first()
                if bank:
                    source_bank_name = bank.bank_name
            
            transaction_list.append({
                'source_bank_name': source_bank_name,
                'source_account_number': t.source_account_number,
                'source_account_name': t.source_account_name,
                'transfer_date': t.transfer_date,
                'transfer_time': t.transfer_time,
                'transfer_amount': t.transfer_amount,
                'note': t.note,
            })
    
    # แปลงข้อมูลเป็น dict
    non_bank_data = {
        'document_number': non_bank_account.document_number,
        'document_date': non_bank_account.document_date,
        'provider_name': provider_name,
        'account_number': non_bank_account.account_number,
        'account_name': non_bank_account.account_name,
        'time_period': non_bank_account.time_period,
        'delivery_date': non_bank_account.delivery_date,
    }
    
    case_data = {
        'case_id': criminal_case.case_id,
        'case_number': criminal_case.case_number,
        'complainant': criminal_case.complainant,
        'victim_name': criminal_case.complainant,  # ใช้ complainant แทน victim_name
        'case_type': criminal_case.case_type,
        'damage_amount': criminal_case.damage_amount,
    }
    
    # สร้าง HTML (ส่ง freeze_account ที่ได้จาก parameter)
    html_content = non_bank_summons_generator.generate_bank_letter_html(
        non_bank_data, 
        case_data, 
        freeze_account,  # ใช้ค่าจาก parameter
        transactions=transaction_list  # ส่งรายการโอนไปด้วย
    )
    
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
    
    # ดึงข้อมูลผู้ให้บริการจาก non_banks table
    provider_name = ''
    non_bank_address = None
    
    if non_bank_account.non_bank_id:
        non_bank = db.query(NonBank).filter(NonBank.id == non_bank_account.non_bank_id).first()
        if non_bank:
            provider_name = non_bank.company_name
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
    
    # แปลงข้อมูลเป็น dict
    non_bank_data = {
        'document_number': non_bank_account.document_number,
        'provider_name': provider_name,
    }
    
    # สร้าง HTML
    html_content = non_bank_summons_generator.generate_envelope_html(non_bank_data, non_bank_address)
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")
        
# ==================== Payment Gateway Summons Endpoints ====================

@router.get("/payment-gateway-summons/{payment_gateway_account_id}", response_class=HTMLResponse)
def generate_payment_gateway_summons_html(
    payment_gateway_account_id: int,
    freeze_account: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างหมายเรียกผู้ให้บริการ Payment Gateway (HTML)"""
    from app.models.payment_gateway_account import PaymentGatewayAccount
    from app.models.payment_gateway import PaymentGateway
    from app.models.payment_gateway_transaction import PaymentGatewayTransaction
    from app.models.bank import Bank
    
    # ดึงข้อมูลบัญชี Payment Gateway
    pg_account = db.query(PaymentGatewayAccount).filter(
        PaymentGatewayAccount.id == payment_gateway_account_id
    ).first()
    if not pg_account:
        raise HTTPException(status_code=404, detail="Payment gateway account not found")
    
    # ดึงข้อมูลคดี
    criminal_case = db.query(CriminalCase).filter(
        CriminalCase.id == pg_account.criminal_case_id
    ).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # ดึงข้อมูลผู้ให้บริการจาก payment_gateways table
    provider_name = ''
    if pg_account.payment_gateway_id:
        pg = db.query(PaymentGateway).filter(PaymentGateway.id == pg_account.payment_gateway_id).first()
        if pg:
            provider_name = pg.company_name
    
    # ดึงรายการโอนที่เกี่ยวข้อง (ถ้ามี)
    transactions = db.query(PaymentGatewayTransaction).filter(
        PaymentGatewayTransaction.payment_gateway_account_id == payment_gateway_account_id
    ).order_by(PaymentGatewayTransaction.transfer_date).all()
    
    # แปลงรายการโอนเป็น list of dicts
    transaction_list = []
    if transactions:
        for t in transactions:
            # ดึงชื่อธนาคารต้นทาง
            source_bank_name = ''
            if t.source_bank_id:
                bank = db.query(Bank).filter(Bank.id == t.source_bank_id).first()
                if bank:
                    source_bank_name = bank.bank_name
            
            # ดึงชื่อธนาคารปลายทาง
            destination_bank_name = ''
            if t.destination_bank_id:
                bank = db.query(Bank).filter(Bank.id == t.destination_bank_id).first()
                if bank:
                    destination_bank_name = bank.bank_name
            
            transaction_list.append({
                'source_bank_name': source_bank_name,
                'source_account_number': t.source_account_number,
                'source_account_name': t.source_account_name,
                'destination_bank_name': destination_bank_name,
                'destination_account_number': t.destination_account_number,
                'destination_account_name': t.destination_account_name,
                'transfer_date': t.transfer_date,
                'transfer_time': t.transfer_time,
                'transfer_amount': t.transfer_amount,
                'note': t.note,
            })
    
    # แปลงข้อมูลเป็น dict
    pg_data = {
        'document_number': pg_account.document_number,
        'document_date': pg_account.document_date,
        'provider_name': provider_name,
        'account_number': pg_account.account_number,
        'account_name': pg_account.account_name,
        'time_period': pg_account.time_period,
        'delivery_date': pg_account.delivery_date,
    }
    
    case_data = {
        'case_id': criminal_case.case_id,
        'case_number': criminal_case.case_number,
        'complainant': criminal_case.complainant,
        'victim_name': criminal_case.complainant,
        'case_type': criminal_case.case_type,
        'damage_amount': criminal_case.damage_amount,
    }
    
    # สร้าง HTML
    html_content = payment_gateway_summons_generator.generate_bank_letter_html(
        pg_data, 
        case_data, 
        freeze_account,
        transactions=transaction_list
    )
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")

@router.get("/payment-gateway-envelope/{payment_gateway_account_id}", response_class=HTMLResponse)
def generate_payment_gateway_envelope_html(
    payment_gateway_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างซองหมายเรียกผู้ให้บริการ Payment Gateway (HTML)"""
    from app.models.payment_gateway_account import PaymentGatewayAccount
    from app.models.payment_gateway import PaymentGateway
    
    # ดึงข้อมูลบัญชี Payment Gateway
    pg_account = db.query(PaymentGatewayAccount).filter(
        PaymentGatewayAccount.id == payment_gateway_account_id
    ).first()
    if not pg_account:
        raise HTTPException(status_code=404, detail="Payment gateway account not found")
    
    # ดึงข้อมูลผู้ให้บริการจาก payment_gateways table
    provider_name = ''
    pg_address = None
    
    if pg_account.payment_gateway_id:
        pg = db.query(PaymentGateway).filter(PaymentGateway.id == pg_account.payment_gateway_id).first()
        if pg:
            provider_name = pg.company_name
            pg_address = {
                'company_address': pg.company_address,
                'soi': pg.soi,
                'moo': pg.moo,
                'road': pg.road,
                'sub_district': pg.sub_district,
                'district': pg.district,
                'province': pg.province,
                'postal_code': pg.postal_code,
            }
    
    # แปลงข้อมูลเป็น dict
    pg_data = {
        'document_number': pg_account.document_number,
        'provider_name': provider_name,
    }
    
    # สร้าง HTML
    html_content = payment_gateway_summons_generator.generate_envelope_html(pg_data, pg_address)
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")

# ============================================
# Telco Mobile (โทรศัพท์มือถือ) Document Endpoints
# ============================================

@router.get("/telco-mobile-summons/{telco_account_id}", response_class=HTMLResponse)
def generate_telco_mobile_summons_html(
    telco_account_id: int,
    freeze_account: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างหมายเรียกข้อมูลโทรศัพท์ (HTML) สำหรับรายการเดียว
    
    Args:
        freeze_account: True = อายัดบัญชี, False = ไม่อายัดบัญชี (default)
    """
    
    # ดึงข้อมูลหมายเลขโทรศัพท์
    telco_account = db.query(TelcoMobileAccount).filter(
        TelcoMobileAccount.id == telco_account_id
    ).first()
    if not telco_account:
        raise HTTPException(status_code=404, detail="Telco mobile account not found")
    
    # ดึงข้อมูลคดี
    criminal_case = db.query(CriminalCase).filter(
        CriminalCase.id == telco_account.criminal_case_id
    ).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # ดึงข้อมูล company_name จาก telco_mobile (สำหรับใช้ในเรียน)
    company_name = telco_account.provider_name  # default
    if telco_account.telco_mobile_id:
        telco_mobile = db.query(TelcoMobile).filter(
            TelcoMobile.id == telco_account.telco_mobile_id
        ).first()
        if telco_mobile and telco_mobile.company_name:
            company_name = telco_mobile.company_name
    
    # แปลงข้อมูลเป็น dict
    telco_data = {
        'id': telco_account.id,
        'document_number': telco_account.document_number,
        'document_date': telco_account.document_date,
        'provider_name': telco_account.provider_name,
        'company_name': company_name,  # เพิ่มชื่อเต็ม
        'phone_number': telco_account.phone_number,
        'time_period': telco_account.time_period,
    }
    
    # ใช้ complainant เป็นฟิลด์หลักสำหรับผู้เสียหาย/ผู้กล่าวหา
    complainant_name = criminal_case.complainant or 'ผู้เสียหาย'
    
    case_data = {
        'case_id': criminal_case.case_id,
        'case_number': criminal_case.case_number,
        'complainant': complainant_name,
        'victim_name': complainant_name,  # เพื่อ backward compatibility
    }
    
    # สร้าง HTML
    html_content = telco_mobile_summons_generator.generate_telco_mobile_letter_html(
        telco_data, case_data, freeze_account
    )
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")

@router.get("/telco-mobile-envelope/{telco_account_id}", response_class=HTMLResponse)
def generate_telco_mobile_envelope_html(
    telco_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างซองหมายเรียกข้อมูลโทรศัพท์ (HTML) สำหรับรายการเดียว"""
    
    # ดึงข้อมูลหมายเลขโทรศัพท์
    telco_account = db.query(TelcoMobileAccount).filter(
        TelcoMobileAccount.id == telco_account_id
    ).first()
    if not telco_account:
        raise HTTPException(status_code=404, detail="Telco mobile account not found")
    
    # ดึงข้อมูลคดี
    criminal_case = db.query(CriminalCase).filter(
        CriminalCase.id == telco_account.criminal_case_id
    ).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # ดึงข้อมูลที่อยู่จาก telco_mobile table (ถ้ามี telco_mobile_id)
    telco_address = None
    if telco_account.telco_mobile_id:
        telco_mobile = db.query(TelcoMobile).filter(
            TelcoMobile.id == telco_account.telco_mobile_id
        ).first()
        if telco_mobile:
            telco_address = {
                'company_name': telco_mobile.company_name,
                'company_name_short': telco_mobile.company_name_short,
                'building_name': telco_mobile.building_name,
                'company_address': telco_mobile.company_address,
                'soi': telco_mobile.soi,
                'moo': telco_mobile.moo,
                'road': telco_mobile.road,
                'sub_district': telco_mobile.sub_district,
                'district': telco_mobile.district,
                'province': telco_mobile.province,
                'postal_code': telco_mobile.postal_code,
            }
    
    # แปลงข้อมูลเป็น dict
    telco_data = {
        'id': telco_account.id,
        'document_number': telco_account.document_number,
        'provider_name': telco_account.provider_name,
        'phone_number': telco_account.phone_number,
    }
    
    # สร้าง HTML ซอง (ส่งที่อยู่ไปด้วย)
    html_content = telco_mobile_summons_generator.generate_telco_mobile_envelope_html(
        telco_data, telco_address
    )
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")

# ============================================
# Telco Internet (IP Address) Document Endpoints
# ============================================

@router.get("/telco-internet-summons/{telco_account_id}", response_class=HTMLResponse)
def generate_telco_internet_summons_html(
    telco_account_id: int,
    freeze_account: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างหมายเรียกข้อมูล IP Address (HTML) สำหรับรายการเดียว
    
    Args:
        freeze_account: True = อายัดบัญชี, False = ไม่อายัดบัญชี (default)
    """
    
    # ดึงข้อมูล IP Address
    telco_account = db.query(TelcoInternetAccount).filter(
        TelcoInternetAccount.id == telco_account_id
    ).first()
    if not telco_account:
        raise HTTPException(status_code=404, detail="Telco internet account not found")
    
    # ดึงข้อมูลคดี
    criminal_case = db.query(CriminalCase).filter(
        CriminalCase.id == telco_account.criminal_case_id
    ).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # ดึงข้อมูล company_name จาก telco_internet (สำหรับใช้ในเรียน)
    company_name = telco_account.provider_name  # default
    if telco_account.telco_internet_id:
        telco_internet = db.query(TelcoInternet).filter(
            TelcoInternet.id == telco_account.telco_internet_id
        ).first()
        if telco_internet and telco_internet.company_name:
            company_name = telco_internet.company_name
    
    # แปลงข้อมูลเป็น dict
    telco_data = {
        'id': telco_account.id,
        'document_number': telco_account.document_number,
        'document_date': telco_account.document_date,
        'provider_name': telco_account.provider_name,
        'company_name': company_name,  # เพิ่มชื่อเต็ม
        'ip_address': telco_account.ip_address,
        'datetime_used': telco_account.datetime_used,
    }
    
    # ใช้ complainant เป็นฟิลด์หลักสำหรับผู้เสียหาย/ผู้กล่าวหา
    complainant_name = criminal_case.complainant or 'ผู้เสียหาย'
    
    case_data = {
        'case_id': criminal_case.case_id,
        'case_number': criminal_case.case_number,
        'complainant': complainant_name,
        'victim_name': complainant_name,  # เพื่อ backward compatibility
    }
    
    # สร้าง HTML
    html_content = telco_internet_summons_generator.generate_telco_internet_letter_html(
        telco_data, case_data, freeze_account
    )
    
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")

@router.get("/telco-internet-envelope/{telco_account_id}", response_class=HTMLResponse)
def generate_telco_internet_envelope_html(
    telco_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างซองหมายเรียกข้อมูล IP Address (HTML) สำหรับรายการเดียว"""
    
    # ดึงข้อมูล IP Address
    telco_account = db.query(TelcoInternetAccount).filter(
        TelcoInternetAccount.id == telco_account_id
    ).first()
    if not telco_account:
        raise HTTPException(status_code=404, detail="Telco internet account not found")
    
    # ดึงข้อมูลคดี
    criminal_case = db.query(CriminalCase).filter(
        CriminalCase.id == telco_account.criminal_case_id
    ).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # ดึงข้อมูลที่อยู่จาก telco_internet table (ถ้ามี telco_internet_id)
    telco_address = None
    if telco_account.telco_internet_id:
        telco_internet = db.query(TelcoInternet).filter(
            TelcoInternet.id == telco_account.telco_internet_id
        ).first()
        if telco_internet:
            telco_address = {
                'company_name': telco_internet.company_name,
                'company_name_short': telco_internet.company_name_short,
                'building_name': telco_internet.building_name,
                'company_address': telco_internet.company_address,
                'soi': telco_internet.soi,
                'moo': telco_internet.moo,
                'road': telco_internet.road,
                'sub_district': telco_internet.sub_district,
                'district': telco_internet.district,
                'province': telco_internet.province,
                'postal_code': telco_internet.postal_code,
            }
    
    # แปลงข้อมูลเป็น dict
    telco_data = {
        'id': telco_account.id,
        'document_number': telco_account.document_number,
        'provider_name': telco_account.provider_name,
        'ip_address': telco_account.ip_address,
    }
    
    # สร้าง HTML ซอง (ส่งที่อยู่ไปด้วย)
    html_content = telco_internet_summons_generator.generate_telco_internet_envelope_html(
        telco_data, telco_address
    )

    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")

# ============================================
# Case Report Endpoint
# ============================================

@router.get("/case-report/{criminal_case_id}", response_class=HTMLResponse)
def generate_case_report_html(
    criminal_case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างรายงานคดีแบบสมบูรณ์ (HTML)"""
    from app.models.payment_gateway_account import PaymentGatewayAccount
    from app.models.payment_gateway import PaymentGateway

    # ดึงข้อมูลคดี
    criminal_case = db.query(CriminalCase).filter(
        CriminalCase.id == criminal_case_id
    ).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")

    # แปลงข้อมูลคดีเป็น dict
    case_data = {
        'case_number': criminal_case.case_number,
        'case_id': criminal_case.case_id,
        'complainant': criminal_case.complainant,
        'damage_amount': criminal_case.damage_amount,
        'complaint_date': criminal_case.complaint_date,
        'incident_date': criminal_case.incident_date,
        'status': criminal_case.status,
        'case_type': criminal_case.case_type,
        'court_name': criminal_case.court_name,
    }

    # ดึงรายการบัญชีธนาคาร
    bank_accounts = db.query(BankAccount).filter(
        BankAccount.criminal_case_id == criminal_case_id
    ).all()
    bank_accounts_list = [{
        'bank_name': ba.bank_name,
        'account_number': ba.account_number,
        'account_name': ba.account_name,
        'document_date': ba.document_date,
        'reply_status': ba.reply_status,
    } for ba in bank_accounts]

    # ดึงรายการผู้ต้องหา
    suspects = db.query(Suspect).filter(
        Suspect.criminal_case_id == criminal_case_id
    ).all()
    suspects_list = [{
        'suspect_name': s.suspect_name,
        'suspect_id_card': s.suspect_id_card,
        'document_date': s.document_date,
        'appointment_date': s.appointment_date,
        'reply_status': s.reply_status,
    } for s in suspects]

    # ดึงรายการ Non-Bank
    non_bank_accounts = db.query(NonBankAccount).filter(
        NonBankAccount.criminal_case_id == criminal_case_id
    ).all()
    non_bank_accounts_list = []
    for nba in non_bank_accounts:
        provider_name = ''
        if nba.non_bank_id:
            non_bank = db.query(NonBank).filter(NonBank.id == nba.non_bank_id).first()
            if non_bank:
                provider_name = non_bank.company_name

        non_bank_accounts_list.append({
            'provider_name': provider_name,
            'account_number': nba.account_number,
            'account_name': nba.account_name,
            'document_date': nba.document_date,
            'reply_status': nba.reply_status,
        })

    # ดึงรายการ Payment Gateway
    pg_accounts = db.query(PaymentGatewayAccount).filter(
        PaymentGatewayAccount.criminal_case_id == criminal_case_id
    ).all()
    pg_accounts_list = []
    for pga in pg_accounts:
        provider_name = ''
        if pga.payment_gateway_id:
            pg = db.query(PaymentGateway).filter(PaymentGateway.id == pga.payment_gateway_id).first()
            if pg:
                provider_name = pg.company_name

        pg_accounts_list.append({
            'provider_name': provider_name,
            'account_number': pga.account_number,
            'account_name': pga.account_name,
            'document_date': pga.document_date,
            'reply_status': pga.reply_status,
        })

    # ดึงรายการหมายเลขโทรศัพท์
    telco_mobile_accounts = db.query(TelcoMobileAccount).filter(
        TelcoMobileAccount.criminal_case_id == criminal_case_id
    ).all()
    telco_mobile_list = [{
        'provider_name': tma.provider_name,
        'phone_number': tma.phone_number,
        'document_date': tma.document_date,
        'reply_status': tma.reply_status,
    } for tma in telco_mobile_accounts]

    # ดึงรายการ IP Address
    telco_internet_accounts = db.query(TelcoInternetAccount).filter(
        TelcoInternetAccount.criminal_case_id == criminal_case_id
    ).all()
    telco_internet_list = [{
        'provider_name': tia.provider_name,
        'ip_address': tia.ip_address,
        'document_date': tia.document_date,
        'reply_status': tia.reply_status,
    } for tia in telco_internet_accounts]

    # สร้าง HTML
    html_content = case_report_generator.generate_case_report_html(
        case_data=case_data,
        bank_accounts=bank_accounts_list,
        suspects=suspects_list,
        non_bank_accounts=non_bank_accounts_list,
        payment_gateway_accounts=pg_accounts_list,
        telco_mobile_accounts=telco_mobile_list,
        telco_internet_accounts=telco_internet_list
    )

    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")