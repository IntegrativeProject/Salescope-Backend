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
    restore_user,
)

router = APIRouter(prefix="/users", tags=["users"])


class UsersAPI:
    def create(self, db: Session, payload: UserCreate):
        existing = get_user_by_email(db, payload.email)
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")
        user = create_user(db, payload)
        if user is None:
            raise HTTPException(status_code=400, detail="Role not found")
        return {"message": "User created successfully", "data": user}

    def get(self, db: Session, user_id: int):
        user = get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User fetched successfully", "data": user}

    def list(self, db: Session, skip: int = 0, limit: int = 50):
        users = list_users(db, skip=skip, limit=limit)
        return {"message": "Users fetched successfully", "data": users}

    def update(self, db: Session, user_id: int, payload: UserUpdate):
        user = update_user(db, user_id, payload)
        if user is None:
            # Could be user not found or role not found; we check original existence
            existing = get_user(db, user_id)
            if not existing:
                raise HTTPException(status_code=404, detail="User not found")
            raise HTTPException(status_code=400, detail="Role not found")
        return {"message": "User updated successfully", "data": user}

    def delete(self, db: Session, user_id: int):
        ok = delete_user(db, user_id)
        if not ok:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}

    def restore(self, db: Session, user_id: int):
        user = restore_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User restored successfully", "data": user}


users_api = UsersAPI()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(payload: UserCreate, db: Session = Depends(get_db)):
    return users_api.create(db, payload)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return users_api.get(db, user_id)


@router.get("/", response_model=UsersListResponse)
def list_users_endpoint(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return users_api.list(db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return users_api.update(db, user_id, payload)


@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return users_api.delete(db, user_id)


@router.put("/{user_id}/restore", response_model=UserResponse)
def restore_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return users_api.restore(db, user_id)
