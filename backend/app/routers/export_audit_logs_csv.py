import csv
from io import StringIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.export_audit_logs_data_service import ExportAuditLogsService

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/audit-logs", response_class=StreamingResponse)
def export_audit_logs_csv(db: Session = Depends(get_db)):
    data = ExportAuditLogsService.get_auditLogs(db)

    output = StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "log_id",
            "action_type",
            "table_name",
            "record_id",
            "actor_id",
            "actor_name",
            "action_timestamp",
            "old_data",
        ],
    )
    writer.writeheader()
    for row in data:
        writer.writerow(row)

    output.seek(0)
    headers = {"Content-Disposition": 'attachment; filename="audit_logs.csv"'}

    return StreamingResponse(output, media_type="text/csv", headers=headers)
