from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.users import (
    UserCreate,
    UserUpdate,
    UserRead,
    UserResponse,
    UsersListResponse,
    MessageResponse,
)
from ..services.users import (
    create_user,
    get_user,
    get_user_by_email,
    list_users,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(payload: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = create_user(db, payload)
    if user is None:
        raise HTTPException(status_code=400, detail="Role not found")
    return {"message": "User created successfully", "data": user}


@router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User fetched successfully", "data": user}


@router.get("/", response_model=UsersListResponse)
def list_users_endpoint(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    users = list_users(db, skip=skip, limit=limit)
    return {"message": "Users fetched successfully", "data": users}


@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = update_user(db, user_id, payload)
    if user is None:
        # Could be user not found or role not found; we check original existence
        existing = get_user(db, user_id)
        if not existing:
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=400, detail="Role not found")
    return {"message": "User updated successfully", "data": user}


@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    ok = delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
