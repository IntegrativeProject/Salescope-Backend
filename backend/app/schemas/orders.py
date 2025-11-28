from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemIn]


class OrderUpdate(BaseModel):
    status: Optional[str] = None  # 'pending', 'paid', 'shipped', 'cancelled'
    # Items update could be added later if needed


class OrderItemRead(BaseModel):
    order_item_id: int
    product_id: int
    quantity: int
    total_price: Optional[float] = None

    class Config:
        from_attributes = True


class OrderRead(BaseModel):
    order_id: int
    user_id: int
    status: str
    total_amount: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    items: List[OrderItemRead] = []

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    message: str
    data: Optional[OrderRead] = None


class OrdersListResponse(BaseModel):
    message: str
    data: List[OrderRead]


class MessageResponse(BaseModel):
    message: str
