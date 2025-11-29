from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.orders import Order
from ..models.order_item import OrderItem
from ..models.products import Product
from ..schemas.orders import OrderCreate, OrderUpdate


class OrderService:
    def __init__(self, db: Session) -> None:
        self.db = db

    # Creation -------------------------------------------------
    def create(self, data: OrderCreate) -> Order:
        order = Order(user_id=data.user_id, status="pending")
        self.db.add(order)
        self.db.flush()  # get order_id for items

        order_total = 0

        for it in data.items:
            product = (
                self.db.query(Product)
                .filter(Product.product_id == it.product_id, Product.is_active == True)
                .first()
            )
            if not product:
                raise ValueError(f"Product {it.product_id} not found or inactive")

            line_total = product.price * it.quantity
            order_total += line_total

            item = OrderItem(
                order_id=order.order_id,
                product_id=it.product_id,
                quantity=it.quantity,
                total_price=line_total,
            )
            self.db.add(item)

        order.total_amount = order_total

        self.db.commit()
        self.db.refresh(order)
        order.items  # ensure relationship is loaded
        return order

    # Read -----------------------------------------------------
    def get(self, order_id: int) -> Optional[Order]:
        return (
            self.db.query(Order)
            .filter(
                Order.order_id == order_id,
                Order.is_active == True,
                Order.deleted_at.is_(None),
            )
            .first()
        )

    def list(self, skip: int = 0, limit: int = 50) -> List[Order]:
        return (
            self.db.query(Order)
            .filter(Order.is_active == True, Order.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )

    # Update ---------------------------------------------------
    def update(self, order_id: int, data: OrderUpdate) -> Optional[Order]:
        order = self.get(order_id)
        if not order:
            return None
        if data.status is not None:
            order.status = data.status
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    # Soft delete / restore ------------------------------------
    def soft_delete(self, order_id: int) -> bool:
        order = self.get(order_id)
        if not order:
            return False
        order.is_active = False
        order.deleted_at = func.now()
        # order.deleted_by can be set later from auth context
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return True

    def restore(self, order_id: int) -> Optional[Order]:
        order = self.db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            return None
        order.is_active = True
        order.deleted_at = None
        order.deleted_by = None
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
