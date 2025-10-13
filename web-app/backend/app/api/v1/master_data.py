from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.core import get_db
from app.api.v1.auth import get_current_user, require_admin
from app.models.user import User
from app.models.bank import Bank
from app.models.non_bank import NonBank
from app.models.payment_gateway import PaymentGateway
from app.models.telco_mobile import TelcoMobile
from app.models.telco_internet import TelcoInternet
from app.models.exchange import Exchange
from app.schemas.bank import Bank as BankSchema, BankCreate, BankUpdate
from app.schemas.non_bank import NonBankResponse as NonBankSchema, NonBankCreate, NonBankUpdate
from app.schemas.payment_gateway import PaymentGateway as PaymentGatewaySchema, PaymentGatewayCreate, PaymentGatewayUpdate
from app.schemas.telco_mobile import TelcoMobileResponse as TelcoMobileSchema, TelcoMobileCreate, TelcoMobileUpdate
from app.schemas.telco_internet import TelcoInternetResponse as TelcoInternetSchema, TelcoInternetCreate, TelcoInternetUpdate
from app.schemas.exchange import ExchangeResponse as ExchangeSchema, ExchangeCreate, ExchangeUpdate

router = APIRouter()


# ==================== Banks ====================

@router.get("/banks", response_model=List[BankSchema])
def get_all_banks(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ดึงรายการธนาคารทั้งหมด (Admin only)"""
    banks = db.query(Bank).order_by(Bank.bank_name).all()
    return banks


@router.get("/banks/{bank_id}", response_model=BankSchema)
def get_bank(
    bank_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ดึงข้อมูลธนาคารตาม ID (Admin only)"""
    bank = db.query(Bank).filter(Bank.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank


@router.post("/banks", response_model=BankSchema)
def create_bank(
    bank: BankCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """สร้างธนาคารใหม่ (Admin only)"""
    # ตรวจสอบว่าชื่อซ้ำหรือไม่
    existing = db.query(Bank).filter(Bank.bank_name == bank.bank_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bank name already exists")

    db_bank = Bank(**bank.dict())
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank


@router.put("/banks/{bank_id}", response_model=BankSchema)
def update_bank(
    bank_id: int,
    bank: BankUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """แก้ไขข้อมูลธนาคาร (Admin only)"""
    db_bank = db.query(Bank).filter(Bank.id == bank_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    # ตรวจสอบชื่อซ้ำ (ถ้ามีการเปลี่ยนชื่อ)
    if bank.bank_name and bank.bank_name != db_bank.bank_name:
        existing = db.query(Bank).filter(Bank.bank_name == bank.bank_name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Bank name already exists")

    update_data = bank.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_bank, key, value)

    db.commit()
    db.refresh(db_bank)
    return db_bank


@router.delete("/banks/{bank_id}")
def delete_bank(
    bank_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ลบธนาคาร (Admin only)"""
    db_bank = db.query(Bank).filter(Bank.id == bank_id).first()
    if not db_bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    # ตรวจสอบว่ามีบัญชีธนาคารที่เชื่อมโยงอยู่หรือไม่
    from app.models.bank_account import BankAccount
    account_count = db.query(func.count(BankAccount.id)).filter(
        BankAccount.bank_id == bank_id
    ).scalar()

    if account_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete bank. {account_count} bank account(s) are linked to this bank."
        )

    db.delete(db_bank)
    db.commit()
    return {"message": "Bank deleted successfully"}


# ==================== Non-Banks ====================

@router.get("/non-banks", response_model=List[NonBankSchema])
def get_all_non_banks(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ดึงรายการ Non-Bank ทั้งหมด (Admin only)"""
    non_banks = db.query(NonBank).order_by(NonBank.company_name).all()
    return non_banks


@router.get("/non-banks/{non_bank_id}", response_model=NonBankSchema)
def get_non_bank(
    non_bank_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ดึงข้อมูล Non-Bank ตาม ID (Admin only)"""
    non_bank = db.query(NonBank).filter(NonBank.id == non_bank_id).first()
    if not non_bank:
        raise HTTPException(status_code=404, detail="Non-Bank not found")
    return non_bank


@router.post("/non-banks", response_model=NonBankSchema)
def create_non_bank(
    non_bank: NonBankCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """สร้าง Non-Bank ใหม่ (Admin only)"""
    existing = db.query(NonBank).filter(NonBank.company_name == non_bank.company_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Non-Bank name already exists")

    db_non_bank = NonBank(**non_bank.dict())
    db.add(db_non_bank)
    db.commit()
    db.refresh(db_non_bank)
    return db_non_bank


@router.put("/non-banks/{non_bank_id}", response_model=NonBankSchema)
def update_non_bank(
    non_bank_id: int,
    non_bank: NonBankUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """แก้ไขข้อมูล Non-Bank (Admin only)"""
    db_non_bank = db.query(NonBank).filter(NonBank.id == non_bank_id).first()
    if not db_non_bank:
        raise HTTPException(status_code=404, detail="Non-Bank not found")

    if non_bank.company_name and non_bank.company_name != db_non_bank.company_name:
        existing = db.query(NonBank).filter(NonBank.company_name == non_bank.company_name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Non-Bank name already exists")

    update_data = non_bank.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_non_bank, key, value)

    db.commit()
    db.refresh(db_non_bank)
    return db_non_bank


@router.delete("/non-banks/{non_bank_id}")
def delete_non_bank(
    non_bank_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ลบ Non-Bank (Admin only)"""
    db_non_bank = db.query(NonBank).filter(NonBank.id == non_bank_id).first()
    if not db_non_bank:
        raise HTTPException(status_code=404, detail="Non-Bank not found")

    from app.models.non_bank_account import NonBankAccount
    account_count = db.query(func.count(NonBankAccount.id)).filter(
        NonBankAccount.non_bank_id == non_bank_id
    ).scalar()

    if account_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete Non-Bank. {account_count} account(s) are linked to this Non-Bank."
        )

    db.delete(db_non_bank)
    db.commit()
    return {"message": "Non-Bank deleted successfully"}


# ==================== Payment Gateways ====================

@router.get("/payment-gateways", response_model=List[PaymentGatewaySchema])
def get_all_payment_gateways(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ดึงรายการ Payment Gateway ทั้งหมด (Admin only)"""
    payment_gateways = db.query(PaymentGateway).order_by(PaymentGateway.company_name).all()
    return payment_gateways


@router.get("/payment-gateways/{payment_gateway_id}", response_model=PaymentGatewaySchema)
def get_payment_gateway(
    payment_gateway_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ดึงข้อมูล Payment Gateway ตาม ID (Admin only)"""
    payment_gateway = db.query(PaymentGateway).filter(PaymentGateway.id == payment_gateway_id).first()
    if not payment_gateway:
        raise HTTPException(status_code=404, detail="Payment Gateway not found")
    return payment_gateway


@router.post("/payment-gateways", response_model=PaymentGatewaySchema)
def create_payment_gateway(
    payment_gateway: PaymentGatewayCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """สร้าง Payment Gateway ใหม่ (Admin only)"""
    existing = db.query(PaymentGateway).filter(
        PaymentGateway.company_name == payment_gateway.company_name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Payment Gateway name already exists")

    db_payment_gateway = PaymentGateway(**payment_gateway.dict())
    db.add(db_payment_gateway)
    db.commit()
    db.refresh(db_payment_gateway)
    return db_payment_gateway


@router.put("/payment-gateways/{payment_gateway_id}", response_model=PaymentGatewaySchema)
def update_payment_gateway(
    payment_gateway_id: int,
    payment_gateway: PaymentGatewayUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """แก้ไขข้อมูล Payment Gateway (Admin only)"""
    db_payment_gateway = db.query(PaymentGateway).filter(
        PaymentGateway.id == payment_gateway_id
    ).first()
    if not db_payment_gateway:
        raise HTTPException(status_code=404, detail="Payment Gateway not found")

    if payment_gateway.company_name and payment_gateway.company_name != db_payment_gateway.company_name:
        existing = db.query(PaymentGateway).filter(
            PaymentGateway.company_name == payment_gateway.company_name
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Payment Gateway name already exists")

    update_data = payment_gateway.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_payment_gateway, key, value)

    db.commit()
    db.refresh(db_payment_gateway)
    return db_payment_gateway


@router.delete("/payment-gateways/{payment_gateway_id}")
def delete_payment_gateway(
    payment_gateway_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ลบ Payment Gateway (Admin only)"""
    db_payment_gateway = db.query(PaymentGateway).filter(
        PaymentGateway.id == payment_gateway_id
    ).first()
    if not db_payment_gateway:
        raise HTTPException(status_code=404, detail="Payment Gateway not found")

    from app.models.payment_gateway_account import PaymentGatewayAccount
    account_count = db.query(func.count(PaymentGatewayAccount.id)).filter(
        PaymentGatewayAccount.payment_gateway_id == payment_gateway_id
    ).scalar()

    if account_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete Payment Gateway. {account_count} account(s) are linked to this Payment Gateway."
        )

    db.delete(db_payment_gateway)
    db.commit()
    return {"message": "Payment Gateway deleted successfully"}


# ==================== Telco Mobile ====================

@router.get("/telco-mobile", response_model=List[TelcoMobileSchema])
def get_all_telco_mobile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ดึงรายการผู้ให้บริการโทรศัพท์มือถือทั้งหมด (Admin only)"""
    telco_mobile = db.query(TelcoMobile).order_by(TelcoMobile.company_name).all()
    return telco_mobile


@router.get("/telco-mobile/{telco_mobile_id}", response_model=TelcoMobileSchema)
def get_telco_mobile(
    telco_mobile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ดึงข้อมูลผู้ให้บริการโทรศัพท์มือถือตาม ID (Admin only)"""
    telco_mobile = db.query(TelcoMobile).filter(TelcoMobile.id == telco_mobile_id).first()
    if not telco_mobile:
        raise HTTPException(status_code=404, detail="Telco Mobile provider not found")
    return telco_mobile


@router.post("/telco-mobile", response_model=TelcoMobileSchema)
def create_telco_mobile(
    telco_mobile: TelcoMobileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """สร้างผู้ให้บริการโทรศัพท์มือถือใหม่ (Admin only)"""
    existing = db.query(TelcoMobile).filter(
        TelcoMobile.company_name == telco_mobile.company_name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Telco Mobile provider name already exists")

    db_telco_mobile = TelcoMobile(**telco_mobile.dict())
    db.add(db_telco_mobile)
    db.commit()
    db.refresh(db_telco_mobile)
    return db_telco_mobile


@router.put("/telco-mobile/{telco_mobile_id}", response_model=TelcoMobileSchema)
def update_telco_mobile(
    telco_mobile_id: int,
    telco_mobile: TelcoMobileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """แก้ไขข้อมูลผู้ให้บริการโทรศัพท์มือถือ (Admin only)"""
    db_telco_mobile = db.query(TelcoMobile).filter(TelcoMobile.id == telco_mobile_id).first()
    if not db_telco_mobile:
        raise HTTPException(status_code=404, detail="Telco Mobile provider not found")

    if telco_mobile.company_name and telco_mobile.company_name != db_telco_mobile.company_name:
        existing = db.query(TelcoMobile).filter(
            TelcoMobile.company_name == telco_mobile.company_name
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Telco Mobile provider name already exists")

    update_data = telco_mobile.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_telco_mobile, key, value)

    db.commit()
    db.refresh(db_telco_mobile)
    return db_telco_mobile


@router.delete("/telco-mobile/{telco_mobile_id}")
def delete_telco_mobile(
    telco_mobile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ลบผู้ให้บริการโทรศัพท์มือถือ (Admin only)"""
    db_telco_mobile = db.query(TelcoMobile).filter(TelcoMobile.id == telco_mobile_id).first()
    if not db_telco_mobile:
        raise HTTPException(status_code=404, detail="Telco Mobile provider not found")

    from app.models.telco_mobile_account import TelcoMobileAccount
    account_count = db.query(func.count(TelcoMobileAccount.id)).filter(
        TelcoMobileAccount.telco_mobile_id == telco_mobile_id
    ).scalar()

    if account_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete Telco Mobile provider. {account_count} account(s) are linked to this provider."
        )

    db.delete(db_telco_mobile)
    db.commit()
    return {"message": "Telco Mobile provider deleted successfully"}


# ==================== Telco Internet ====================

@router.get("/telco-internet", response_model=List[TelcoInternetSchema])
def get_all_telco_internet(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ดึงรายการผู้ให้บริการอินเทอร์เน็ตทั้งหมด (Admin only)"""
    telco_internet = db.query(TelcoInternet).order_by(TelcoInternet.company_name).all()
    return telco_internet


@router.get("/telco-internet/{telco_internet_id}", response_model=TelcoInternetSchema)
def get_telco_internet(
    telco_internet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ดึงข้อมูลผู้ให้บริการอินเทอร์เน็ตตาม ID (Admin only)"""
    telco_internet = db.query(TelcoInternet).filter(TelcoInternet.id == telco_internet_id).first()
    if not telco_internet:
        raise HTTPException(status_code=404, detail="Telco Internet provider not found")
    return telco_internet


@router.post("/telco-internet", response_model=TelcoInternetSchema)
def create_telco_internet(
    telco_internet: TelcoInternetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """สร้างผู้ให้บริการอินเทอร์เน็ตใหม่ (Admin only)"""
    existing = db.query(TelcoInternet).filter(
        TelcoInternet.company_name == telco_internet.company_name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Telco Internet provider name already exists")

    db_telco_internet = TelcoInternet(**telco_internet.dict())
    db.add(db_telco_internet)
    db.commit()
    db.refresh(db_telco_internet)
    return db_telco_internet


@router.put("/telco-internet/{telco_internet_id}", response_model=TelcoInternetSchema)
def update_telco_internet(
    telco_internet_id: int,
    telco_internet: TelcoInternetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """แก้ไขข้อมูลผู้ให้บริการอินเทอร์เน็ต (Admin only)"""
    db_telco_internet = db.query(TelcoInternet).filter(
        TelcoInternet.id == telco_internet_id
    ).first()
    if not db_telco_internet:
        raise HTTPException(status_code=404, detail="Telco Internet provider not found")

    if telco_internet.company_name and telco_internet.company_name != db_telco_internet.company_name:
        existing = db.query(TelcoInternet).filter(
            TelcoInternet.company_name == telco_internet.company_name
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Telco Internet provider name already exists")

    update_data = telco_internet.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_telco_internet, key, value)

    db.commit()
    db.refresh(db_telco_internet)
    return db_telco_internet


@router.delete("/telco-internet/{telco_internet_id}")
def delete_telco_internet(
    telco_internet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ลบผู้ให้บริการอินเทอร์เน็ต (Admin only)"""
    db_telco_internet = db.query(TelcoInternet).filter(
        TelcoInternet.id == telco_internet_id
    ).first()
    if not db_telco_internet:
        raise HTTPException(status_code=404, detail="Telco Internet provider not found")

    from app.models.telco_internet_account import TelcoInternetAccount
    account_count = db.query(func.count(TelcoInternetAccount.id)).filter(
        TelcoInternetAccount.telco_internet_id == telco_internet_id
    ).scalar()

    if account_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete Telco Internet provider. {account_count} account(s) are linked to this provider."
        )

    db.delete(db_telco_internet)
    db.commit()
    return {"message": "Telco Internet provider deleted successfully"}


# ==================== Exchanges ====================

@router.get("/exchanges", response_model=List[ExchangeSchema])
def get_all_exchanges(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ดึงรายการ Exchange ทั้งหมด (Admin only)"""
    exchanges = db.query(Exchange).order_by(Exchange.company_name).all()
    return exchanges


@router.get("/exchanges/{exchange_id}", response_model=ExchangeSchema)
def get_exchange(
    exchange_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ดึงข้อมูล Exchange ตาม ID (Admin only)"""
    exchange = db.query(Exchange).filter(Exchange.id == exchange_id).first()
    if not exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")
    return exchange


@router.post("/exchanges", response_model=ExchangeSchema)
def create_exchange(
    exchange: ExchangeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """สร้าง Exchange ใหม่ (Admin only)"""
    existing = db.query(Exchange).filter(Exchange.company_name == exchange.company_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Exchange name already exists")

    db_exchange = Exchange(**exchange.dict())
    db.add(db_exchange)
    db.commit()
    db.refresh(db_exchange)
    return db_exchange


@router.put("/exchanges/{exchange_id}", response_model=ExchangeSchema)
def update_exchange(
    exchange_id: int,
    exchange: ExchangeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """แก้ไขข้อมูล Exchange (Admin only)"""
    db_exchange = db.query(Exchange).filter(Exchange.id == exchange_id).first()
    if not db_exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")

    if exchange.company_name and exchange.company_name != db_exchange.company_name:
        existing = db.query(Exchange).filter(Exchange.company_name == exchange.company_name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Exchange name already exists")

    update_data = exchange.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_exchange, key, value)

    db.commit()
    db.refresh(db_exchange)
    return db_exchange


@router.delete("/exchanges/{exchange_id}")
def delete_exchange(
    exchange_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """ลบ Exchange (Admin only) - ปัจจุบันยังไม่มีตาราง exchange_accounts"""
    db_exchange = db.query(Exchange).filter(Exchange.id == exchange_id).first()
    if not db_exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")

    db.delete(db_exchange)
    db.commit()
    return {"message": "Exchange deleted successfully"}
