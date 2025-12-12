from typing import List, Dict, Any
from sqlalchemy.orm import Session

from ..models import Product


class ExportProductDataService:
    @staticmethod
    def get_products_for_export(db: Session) -> List[Dict[str, Any]]:
        products = db.query(Product).all()
        rows: List[Dict[str, Any]] = []
        for p in products:
            rows.append(
                {
                    "product_id": p.product_id,
                    "name": p.name,
                    "description": p.description,
                    "price": float(p.price) if p.price is not None else None,
                    "stock": p.stock,
                    "category": p.category,
                    "is_active": p.is_active,
                    "created_at": p.created_at,
                }
            )
        return rows
