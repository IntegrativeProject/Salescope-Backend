from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.orders import Order
from ..schemas.orders import OrderCreate, OrderUpdate
from .order_service import OrderService


def _service(db: Session) -> OrderService:
    return OrderService(db)


def create_order(db: Session, data: OrderCreate) -> Order:
    return _service(db).create(data)


def get_order(db: Session, order_id: int) -> Optional[Order]:
    return _service(db).get(order_id)


def list_orders(db: Session, skip: int = 0, limit: int = 50) -> List[Order]:
    return _service(db).list(skip=skip, limit=limit)


def update_order(db: Session, order_id: int, data: OrderUpdate) -> Optional[Order]:
    return _service(db).update(order_id, data)


def delete_order(db: Session, order_id: int) -> bool:
    return _service(db).soft_delete(order_id)


def restore_order(db: Session, order_id: int) -> Optional[Order]:
    return _service(db).restore(order_id)
