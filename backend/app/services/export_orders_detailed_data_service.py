from typing import List, Dict, Any

from sqlalchemy.orm import Session

from ..models import Order, OrderItem, Product


class ExportOrdersDetailedDataService:
    @staticmethod
    def get_orders_detailed_for_export(db: Session) -> List[Dict[str, Any]]:
        # Join orders + order_items + products
        query = (
            db.query(
                Order.order_id,
                Order.user_id,
                Order.status,
                Order.total_amount,
                Order.created_at.label("order_created_at"),
                OrderItem.order_item_id,
                OrderItem.quantity,
                OrderItem.total_price,
                Product.product_id,
                Product.name.label("product_name"),
                Product.price.label("product_price"),
            )
            .join(OrderItem, OrderItem.order_id == Order.order_id)
            .join(Product, Product.product_id == OrderItem.product_id)
        )

        rows: List[Dict[str, Any]] = []
        for r in query.all():
            rows.append(
                {
                    "order_id": r.order_id,
                    "user_id": r.user_id,
                    "status": r.status,
                    "order_total_amount": float(r.total_amount) if r.total_amount is not None else None,
                    "order_created_at": r.order_created_at,
                    "order_item_id": r.order_item_id,
                    "quantity": r.quantity,
                    "order_item_total_price": float(r.total_price) if r.total_price is not None else None,
                    "product_id": r.product_id,
                    "product_name": r.product_name,
                    "product_price": float(r.product_price) if r.product_price is not None else None,
                }
            )

        return rows
