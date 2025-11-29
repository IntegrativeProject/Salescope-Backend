from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from ..models.order_item import OrderItem
from ..models.orders import Order
from ..models.products import Product
from ..schemas.order_item import OrderItemCreate, OrderItemUpdate, OrderItemInDB


class OrderItemService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _recompute_order_total(self, order_id: int) -> None:
        # Recompute sum of all items and persist in Order.total_amount
        total = (
            self.db.query(func.coalesce(func.sum(OrderItem.total_price), 0))
            .filter(OrderItem.order_id == order_id)
            .scalar()
        )
        order = self.db.query(Order).filter(Order.order_id == order_id).first()
        if order:
            order.total_amount = total
            self.db.add(order)

    def create(self, order_id: int, data: OrderItemCreate) -> OrderItemInDB:
        try:
            # Validate order exists and is active/not deleted
            order = (
                self.db.query(Order)
                .filter(
                    Order.order_id == order_id,
                    Order.is_active == True,
                    Order.deleted_at.is_(None),
                )
                .first()
            )
            if not order:
                raise ValueError(f"Order {order_id} not found or inactive")

            # Validate product exists and is active
            product = (
                self.db.query(Product)
                .filter(Product.product_id == data.product_id, Product.is_active == True)
                .first()
            )
            if not product:
                raise ValueError(f"Product {data.product_id} not found or inactive")

            line_total = product.price * data.quantity
            item = OrderItem(
                order_id=order_id,
                product_id=data.product_id,
                quantity=data.quantity,
                total_price=line_total,
            )
            self.db.add(item)

            # Update order total
            self._recompute_order_total(order_id)

            self.db.commit()
            self.db.refresh(item)
            return OrderItemInDB.model_validate(item)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise

    def get(self, order_item_id: int) -> Optional[OrderItemInDB]:
        item = (
            self.db.query(OrderItem)
            .filter(OrderItem.order_item_id == order_item_id)
            .first()
        )
        return OrderItemInDB.model_validate(item) if item else None

    def list_by_order(self, order_id: int) -> List[OrderItemInDB]:
        items = self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        return [OrderItemInDB.model_validate(i) for i in items]

    def update(self, order_item_id: int, data: OrderItemUpdate) -> Optional[OrderItemInDB]:
        try:
            item = (
                self.db.query(OrderItem)
                .filter(OrderItem.order_item_id == order_item_id)
                .first()
            )
            if not item:
                return None

            if data.quantity is not None:
                # Recompute line total from product price
                product = self.db.query(Product).filter(Product.product_id == item.product_id).first()
                if not product or product.is_active is False:
                    raise ValueError(f"Product {item.product_id} not found or inactive")
                item.quantity = data.quantity
                item.total_price = product.price * item.quantity

            order_id = item.order_id
            self.db.add(item)

            # Update order total
            self._recompute_order_total(order_id)

            self.db.commit()
            self.db.refresh(item)
            return OrderItemInDB.model_validate(item)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, order_item_id: int) -> bool:
        try:
            item = (
                self.db.query(OrderItem)
                .filter(OrderItem.order_item_id == order_item_id)
                .first()
            )
            if not item:
                return False
            order_id = item.order_id
            self.db.delete(item)

            # Update order total
            self._recompute_order_total(order_id)

            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            return False
