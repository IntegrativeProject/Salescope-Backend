from typing import List, Dict, Any

from sqlalchemy.orm import Session

from ..models import Order


class ExportOrderDataService:
    @staticmethod
    def get_orders_for_export(db: Session) -> List[Dict[str, Any]]:
        orders = db.query(Order).all()
        rows: List[Dict[str, Any]] = []
        for o in orders:
            rows.append(
                {
                    "order_id": o.order_id,
                    "user_id": o.user_id,
                    "status": o.status,
                    "total_amount": float(o.total_amount) if o.total_amount is not None else None,
                    "is_active": o.is_active,
                    "created_at": o.created_at,
                    "updated_at": o.updated_at,
                }
            )
        return rows