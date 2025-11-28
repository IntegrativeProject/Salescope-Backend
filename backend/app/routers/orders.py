from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.orders import (
    OrderCreate,
    OrderUpdate,
    OrderRead,
    OrderResponse,
    OrdersListResponse,
    MessageResponse,
)
from ..services.orders import (
    create_order,
    get_order,
    list_orders,
    update_order,
    delete_order,
)


router = APIRouter(prefix="/orders", tags=["orders"])


class OrdersAPI:
    def create(self, db: Session, payload: OrderCreate):
        order = create_order(db, payload)
        return {"message": "Order created successfully", "data": order}

    def get(self, db: Session, order_id: int):
        order = get_order(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"message": "Order fetched successfully", "data": order}

    def list(self, db: Session, skip: int = 0, limit: int = 50):
        orders = list_orders(db, skip=skip, limit=limit)
        return {"message": "Orders fetched successfully", "data": orders}

    def update(self, db: Session, order_id: int, payload: OrderUpdate):
        order = update_order(db, order_id, payload)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"message": "Order updated successfully", "data": order}

    def delete(self, db: Session, order_id: int):
        ok = delete_order(db, order_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"message": "Order deleted successfully"}


orders_api = OrdersAPI()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_endpoint(payload: OrderCreate, db: Session = Depends(get_db)):
    return orders_api.create(db, payload)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    return orders_api.get(db, order_id)


@router.get("/", response_model=OrdersListResponse)
def list_orders_endpoint(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return orders_api.list(db, skip=skip, limit=limit)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order_endpoint(order_id: int, payload: OrderUpdate, db: Session = Depends(get_db)):
    return orders_api.update(db, order_id, payload)


@router.delete("/{order_id}", response_model=MessageResponse)
def delete_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    return orders_api.delete(db, order_id)
