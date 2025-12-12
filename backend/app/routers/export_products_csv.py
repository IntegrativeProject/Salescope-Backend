import csv
from io import StringIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.export_product_data_service import ExportProductDataService

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/products", response_class=StreamingResponse)
def export_products_csv(db: Session = Depends(get_db)):
    data = ExportProductDataService.get_products_for_export(db)

    output = StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "product_id",
            "name",
            "description",
            "price",
            "stock",
            "category",
            "is_active",
            "created_at",
        ],
    )
    writer.writeheader()
    for row in data:
        writer.writerow(row)

    output.seek(0)
    headers = {"Content-Disposition": 'attachment; filename="products.csv"'}

    return StreamingResponse(output, media_type="text/csv", headers=headers)
