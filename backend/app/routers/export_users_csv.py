import csv
from io import StringIO
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.export_user_data_service import ExportDataService

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/users", response_class=StreamingResponse)
def export_users_csv(db: Session = Depends(get_db)):
    data = ExportDataService.get_users_for_export(db)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        "user_id",
        "full_name",
        "email",
        "is_active",
        "created_at",
    ])
    writer.writeheader()
    for row in data:
        writer.writerow(row)

    output.seek(0)
    headers = {
        "Content-Disposition": 'attachment; filename="users.csv"'
    }

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers=headers,
    )