from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role_name: str = Field(..., description="Role name e.g. 'Customer'")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AuthUser(BaseModel):
    user_id: int
    email: EmailStr
    full_name: str
    role_id: int

class LoginSuccess(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUser
