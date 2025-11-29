from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.orders import Order
from ..models.order_item import OrderItem
from ..schemas.orders import OrderCreate, OrderUpdate


def create_order(db: Session, data: OrderCreate) -> Order:
    order = Order(user_id=data.user_id, status="pending")
    db.add(order)
    db.flush()  # get order_id for items

    for it in data.items:
        item = OrderItem(
            order_id=order.order_id,
            product_id=it.product_id,
            quantity=it.quantity,
        )
        db.add(item)

    db.commit()
    db.refresh(order)
    # Load items
    order.items  # access relationship to ensure it's available
    return order


def get_order(db: Session, order_id: int) -> Optional[Order]:
    return (
        db.query(Order)
        .filter(
            Order.order_id == order_id,
            Order.is_active == True,
            Order.deleted_at.is_(None),
        )
        .first()
    )


def list_orders(db: Session, skip: int = 0, limit: int = 50) -> List[Order]:
    return (
        db.query(Order)
        .filter(Order.is_active == True, Order.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
        .all()
    )


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
    order.is_active = False
    order.deleted_at = func.now()
    # order.deleted_by can be set later from auth context
    db.add(order)
    db.commit()
    db.refresh(order)
    return True


def restore_order(db: Session, order_id: int) -> Optional[Order]:
    # Query without soft-delete filters to allow restoring
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return None
    order.is_active = True
    order.deleted_at = None
    order.deleted_by = None
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
