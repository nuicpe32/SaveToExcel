from fastapi import APIRouter
from . import auth, bank_accounts, suspects, criminal_cases, post_arrests, documents, case_types
from .endpoints import banks

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(banks.router, prefix="/banks", tags=["banks"])
api_router.include_router(bank_accounts.router, prefix="/bank-accounts", tags=["bank-accounts"])
api_router.include_router(suspects.router, prefix="/suspects", tags=["suspects"])
api_router.include_router(criminal_cases.router, prefix="/criminal-cases", tags=["criminal-cases"])
api_router.include_router(post_arrests.router, prefix="/post-arrests", tags=["post-arrests"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(case_types.router, tags=["case-types"])