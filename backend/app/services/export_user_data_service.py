from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models import User

class ExportDataService:
    @staticmethod
    def get_users_for_export(db: Session) -> List[Dict[str, Any]]:
        users = db.query(User).all()
        rows = []
        for u in users:
            rows.append({
                "user_id": u.user_id,
                "full_name": u.full_name,
                "email": u.email,
                "is_active": u.is_active,
                "created_at": u.created_at,
            })
        return rows