from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models import AuditLog

class ExportAuditLogsService:
    @staticmethod
    def get_auditLogs(db: Session) -> List[Dict[str, Any]]:
        audit_logs = db.query(AuditLog).all()
        rows: List[Dict[str, Any]] = []
        for al in audit_logs:
            rows.append(
                {
                    "log_id": al.log_id,
                    "action_type": al.action_type,
                    "table_name": al.table_name,
                    "record_id": al.record_id,
                    "actor_id": al.actor_id,
                    "actor_name": al.actor_name,
                    "action_timestamp": al.action_timestamp,
                    "old_data": al.old_data,
                }
            )
        return rows
