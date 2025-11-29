from typing import List, Optional
from sqlalchemy.orm import Session

from ..schemas.order_item import OrderItemCreate, OrderItemUpdate, OrderItemInDB
from .order_item_service import OrderItemService


def _service(db: Session) -> OrderItemService:
    return OrderItemService(db)


def create_order_item(db: Session, order_id: int, data: OrderItemCreate) -> OrderItemInDB:
    return _service(db).create(order_id, data)


def get_order_item(db: Session, order_item_id: int) -> Optional[OrderItemInDB]:
    return _service(db).get(order_item_id)


def list_order_items_by_order(db: Session, order_id: int) -> List[OrderItemInDB]:
    return _service(db).list_by_order(order_id)


def update_order_item(db: Session, order_item_id: int, data: OrderItemUpdate) -> Optional[OrderItemInDB]:
    return _service(db).update(order_item_id, data)


def delete_order_item(db: Session, order_item_id: int) -> bool:
    return _service(db).delete(order_item_id)
