import csv
from io import StringIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.export_order_items_data_service import ExportOrderItemService

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/order-items", response_class=StreamingResponse)
def export_order_items_csv(db: Session = Depends(get_db)):
    data = ExportOrderItemService.get_orderItems(db)

    output = StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "total_price",
        ],
    )
    writer.writeheader()
    for row in data:
        writer.writerow(row)

    output.seek(0)
    headers = {"Content-Disposition": 'attachment; filename="order_items.csv"'}

    return StreamingResponse(output, media_type="text/csv", headers=headers)
