from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.orders import Order
from ..models.order_item import OrderItem
from ..schemas.orders import OrderCreate, OrderUpdate


def create_order(db: Session, data: OrderCreate) -> Order:
    order = Order(user_id=data.user_id, status='pending')
    db.add(order)
    db.flush()  # get order_id for items

    for it in data.items:
        item = OrderItem(order_id=order.order_id, product_id=it.product_id, quantity=it.quantity)
        db.add(item)

    db.commit()
    db.refresh(order)
    # Load items
    order.items  # access relationship to ensure it's available
    return order


def get_order(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.order_id == order_id).first()


def list_orders(db: Session, skip: int = 0, limit: int = 50) -> List[Order]:
    return db.query(Order).offset(skip).limit(limit).all()


def update_order(db: Session, order_id: int, data: OrderUpdate) -> Optional[Order]:
    order = get_order(db, order_id)
    if not order:
        return None
    if data.status is not None:
        order.status = data.status
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int) -> bool:
    order = get_order(db, order_id)
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True
