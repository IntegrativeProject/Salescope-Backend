import csv
from io import StringIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.export_orders_detailed_data_service import ExportOrdersDetailedDataService

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/orders-detailed", response_class=StreamingResponse)
def export_orders_detailed_csv(db: Session = Depends(get_db)):
    data = ExportOrdersDetailedDataService.get_orders_detailed_for_export(db)

    output = StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "order_id",
            "user_id",
            "status",
            "order_total_amount",
            "order_created_at",
            "order_item_id",
            "quantity",
            "order_item_total_price",
            "product_id",
            "product_name",
            "product_price",
        ],
    )
    writer.writeheader()
    for row in data:
        writer.writerow(row)

    output.seek(0)
    headers = {"Content-Disposition": 'attachment; filename="orders_detailed.csv"'}

    return StreamingResponse(output, media_type="text/csv", headers=headers)
