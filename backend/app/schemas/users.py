from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role_name: str
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password_hash: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role_name: Optional[str] = None
    password_hash: Optional[str] = None
    is_active: Optional[bool] = None


class UserRead(BaseModel):
    user_id: int
    role_id: int
    full_name: str
    email: EmailStr
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    message: str
    data: Optional[UserRead] = None


class UsersListResponse(BaseModel):
    message: str
    data: List[UserRead]


class MessageResponse(BaseModel):
    message: str
