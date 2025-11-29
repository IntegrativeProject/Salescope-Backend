from pydantic import BaseModel, Field
from typing import Optional

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0, description="Quantity must be greater than 0")

class OrderItemInDB(OrderItemBase):
    order_item_id: int
    order_id: int
    total_price: float

    class Config:
        from_attributes = True

class OrderItemResponse(OrderItemInDB):
    pass
