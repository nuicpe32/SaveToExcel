from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BankBase(BaseModel):
    bank_name: str
    bank_address: Optional[str] = None
    soi: Optional[str] = None
    moo: Optional[str] = None
    road: Optional[str] = None
    sub_district: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None


class BankCreate(BankBase):
    pass


class BankUpdate(BaseModel):
    bank_name: Optional[str] = None
    bank_address: Optional[str] = None
    soi: Optional[str] = None
    moo: Optional[str] = None
    road: Optional[str] = None
    sub_district: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None


class Bank(BankBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
