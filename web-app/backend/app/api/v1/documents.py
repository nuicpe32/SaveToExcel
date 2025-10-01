from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core import get_db
from app.models import User, BankAccount, Suspect
from app.services import DocumentGenerator
from app.api.v1.auth import get_current_user
import os

router = APIRouter()

doc_generator = DocumentGenerator()

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

@router.get("/suspect-summons/{suspect_id}")
def generate_suspect_summons_document(
    suspect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    if not suspect:
        raise HTTPException(status_code=404, detail="Suspect not found")

    data = {
        "document_number": suspect.document_number,
        "full_name": suspect.full_name,
        "charge": suspect.charge,
        "case_number": suspect.case_number,
        "summons_location": suspect.summons_location,
        "summons_date": suspect.summons_date,
        "summons_time": suspect.summons_time
    }

    filepath = doc_generator.generate_suspect_summons_doc(data)

    return FileResponse(
        path=filepath,
        filename=os.path.basename(filepath),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )