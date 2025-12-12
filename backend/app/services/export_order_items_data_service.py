from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models import OrderItem

class ExportOrderItemService:
    @staticmethod
    def get_orderItems(db: Session) -> List[Dict[str, Any]]:
        orderItems = db.query(OrderItem).all()
        rows: List[Dict[str, Any]] = []
        for oi in orderItems:
            rows.append(
                {
                    "order_item_id": oi.order_item_id,
                    "order_id": oi.order_id,
                    "product_id": oi.product_id,
                    "quantity": oi.quantity,
                    "total_price": float(oi.total_price) if oi.total_price is not None else None,
                }
            )
        return rows

