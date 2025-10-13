from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload
from datetime import timedelta, datetime
from app.core import get_db, verify_password, get_password_hash, create_access_token, settings
from app.models import User
from app.schemas import Token, UserCreate, UserResponse

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from app.core.security import decode_access_token

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = db.query(User).options(
        joinedload(User.rank),
        joinedload(User.role),
        joinedload(User.bureau),
        joinedload(User.division),
        joinedload(User.supervision)
    ).filter(User.username == username).first()
    
    if user is None:
        raise credentials_exception
    
    # Check if user is active and approved
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="บัญชีถูกปิดใช้งาน"
        )
    
    if not user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="บัญชียังไม่ได้รับการอนุมัติ"
        )
    
    # ตรวจสอบสิทธิ์หน่วยงาน (ยกเว้น Admin)
    if user.role and user.role.role_name != 'admin':
        if user.supervision and not user.supervision.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ไม่มีสิทธิ์เข้าใช้งาน กรุณาติดต่อผู้ดูแลระบบ"
            )
        
        if user.division and not user.division.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ไม่มีสิทธิ์เข้าใช้งาน กรุณาติดต่อผู้ดูแลระบบ"
            )
        
        if user.bureau and not user.bureau.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ไม่มีสิทธิ์เข้าใช้งาน กรุณาติดต่อผู้ดูแลระบบ"
            )

    return user

def require_admin(current_user: User = Depends(get_current_user)):
    """ตรวจสอบว่าผู้ใช้มีสิทธิ์ admin หรือไม่"""
    if not current_user.role or current_user.role.role_name != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ไม่มีสิทธิ์เข้าถึงฟังก์ชันนี้ (ต้องเป็น Admin เท่านั้น)"
        )
    return current_user

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Load user with organization data
    user = db.query(User).options(
        joinedload(User.bureau),
        joinedload(User.division),
        joinedload(User.supervision)
    ).filter(User.username == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="บัญชีถูกล็อค กรุณาติดต่อผู้ดูแลระบบ"
        )
    
    # Check if user is approved
    if not user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="บัญชียังไม่ได้รับการอนุมัติจากผู้ดูแลระบบ"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="บัญชีถูกปิดใช้งาน"
        )
    
    # ตรวจสอบสิทธิ์หน่วยงาน (ยกเว้น Admin)
    # Load user role to check if admin
    user_with_role = db.query(User).options(joinedload(User.role)).filter(User.id == user.id).first()
    
    if user_with_role and user_with_role.role and user_with_role.role.role_name != 'admin':
        if user.supervision and not user.supervision.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ไม่มีสิทธิ์เข้าใช้งาน กรุณาติดต่อผู้ดูแลระบบ"
            )
        
        if user.division and not user.division.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ไม่มีสิทธิ์เข้าใช้งาน กรุณาติดต่อผู้ดูแลระบบ"
            )
        
        if user.bureau and not user.bureau.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ไม่มีสิทธิ์เข้าใช้งาน กรุณาติดต่อผู้ดูแลระบบ"
            )
    
    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        # Increment failed login attempts
        user.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts
        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(hours=1)  # Lock for 1 hour
        
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Reset failed login attempts on successful login
    user.failed_login_attempts = 0
    user.locked_until = None
    db.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user