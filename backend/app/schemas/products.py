from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: Optional[str] = None 

class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


class ProductRead(BaseModel):
    product_id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    message: str
    data: Optional[ProductRead] = None


class ProductsListResponse(BaseModel):
    message: str
    data: List[ProductRead]


class MessageResponse(BaseModel):
    message: str