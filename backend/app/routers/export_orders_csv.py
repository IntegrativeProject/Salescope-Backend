import csv
from io import StringIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.export_orders_data_service import ExportOrderDataService

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/orders", response_class=StreamingResponse)
def export_orders_csv(db: Session = Depends(get_db)):
    data = ExportOrderDataService.get_orders_for_export(db)

    output = StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "order_id",
            "user_id",
            "status",
            "total_amount",
            "is_active",
            "created_at",
            "updated_at",
        ],
    )
    writer.writeheader()
    for row in data:
        writer.writerow(row)

    output.seek(0)
    headers = {"Content-Disposition": 'attachment; filename="orders.csv"'}

    return StreamingResponse(output, media_type="text/csv", headers=headers)
