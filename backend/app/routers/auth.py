from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.auth import RegisterRequest, LoginRequest, LoginSuccess, AuthUser
from ..services.users import create_user, get_user_by_email
from ..schemas.users import UserCreate
from ..utils.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"]) 


@router.post("/register", response_model=LoginSuccess, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    # Check existing email
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    pw_hash = hash_password(payload.password)
    # Build schema for existing create_user service
    to_create = UserCreate(
        full_name=payload.full_name,
        email=payload.email,
        role_name=payload.role_name,
        password_hash=pw_hash,
        is_active=True,
    )
    user = create_user(db, to_create)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role not found")

    token = create_access_token({
        "sub": user.email,
        "user_id": user.user_id,
        "role_id": user.role_id,
    })
    return LoginSuccess(
        access_token=token,
        user=AuthUser(user_id=user.user_id, email=user.email, full_name=user.full_name, role_id=user.role_id),
    )


@router.post("/login", response_model=LoginSuccess)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({
        "sub": user.email,
        "user_id": user.user_id,
        "role_id": user.role_id,
    })
    return LoginSuccess(
        access_token=token,
        user=AuthUser(user_id=user.user_id, email=user.email, full_name=user.full_name, role_id=user.role_id),
    )
