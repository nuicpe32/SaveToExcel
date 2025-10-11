from fastapi import APIRouter
from . import auth, bank_accounts, suspects, criminal_cases, post_arrests, documents, case_types, courts, pdf_parser, police_stations, user_registration, admin_users, cfr_upload
from .endpoints import banks, non_banks, telco_mobile, telco_internet, exchanges, organizations

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(user_registration.router, prefix="/registration", tags=["user-registration"])
api_router.include_router(admin_users.router, prefix="/admin", tags=["admin-users"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(banks.router, prefix="/banks", tags=["banks"])
api_router.include_router(non_banks.router, prefix="/non-banks", tags=["non-banks"])
api_router.include_router(telco_mobile.router, prefix="/telco-mobile", tags=["telco-mobile"])
api_router.include_router(telco_internet.router, prefix="/telco-internet", tags=["telco-internet"])
api_router.include_router(exchanges.router, prefix="/exchanges", tags=["exchanges"])
api_router.include_router(courts.router, prefix="/courts", tags=["courts"])
api_router.include_router(bank_accounts.router, prefix="/bank-accounts", tags=["bank-accounts"])
api_router.include_router(suspects.router, prefix="/suspects", tags=["suspects"])
api_router.include_router(criminal_cases.router, prefix="/criminal-cases", tags=["criminal-cases"])
api_router.include_router(post_arrests.router, prefix="/post-arrests", tags=["post-arrests"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(case_types.router, tags=["case-types"])
api_router.include_router(pdf_parser.router, tags=["pdf-parser"])
api_router.include_router(police_stations.router, prefix="/police-stations", tags=["police-stations"])
api_router.include_router(cfr_upload.router, prefix="/cfr", tags=["cfr"])