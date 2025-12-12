from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.analytics import AnalyticsGraphics
from ..schemas.analythics import (
    BestProductResponse,
    TopProductsResponse,
    DailySalesResponse,
    DailySalesByProductResponse,
    WeeklySalesResponse,
    WeeklySalesAverageResponse,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/best-product", response_model=BestProductResponse)
def best_product(db: Session = Depends(get_db)):
    service = AnalyticsGraphics(db)
    row = service.get_best_selling_product()

    if not row:
        return BestProductResponse(message="No sales data", data=None)

    product_id, name, total_sold = row
    return BestProductResponse(
        message="Best selling product fetched successfully",
        data={
            "product_id": product_id,
            "name": name,
            "total_sold": int(total_sold),
        },
    )


@router.get("/top-products", response_model=TopProductsResponse)
def top_products(limit: int = 5, db: Session = Depends(get_db)):
    service = AnalyticsGraphics(db)
    rows = service.get_top_selling_products(limit=limit)

    items = [
        {
            "product_id": r.product_id,
            "name": r.name,
            "total_sold": int(r.total_sold),
        }
        for r in rows
    ]

    return TopProductsResponse(
        message="Top products fetched successfully",
        data=items,
    )


@router.get("/daily-sales", response_model=DailySalesResponse)
def daily_sales(db: Session = Depends(get_db)):
    service = AnalyticsGraphics(db)
    rows = service.get_daily_sales()

    items = [
        {
            "day": r.day,
            "units": int(r.units),
        }
        for r in rows
    ]

    return DailySalesResponse(
        message="Daily sales fetched successfully",
        data=items,
    )


@router.get("/daily-sales-by-product", response_model=DailySalesByProductResponse)
def daily_sales_by_product(db: Session = Depends(get_db)):
    service = AnalyticsGraphics(db)
    rows = service.get_daily_sales_by_product()

    items = [
        {
            "product_id": r.product_id,
            "day": r.day,
            "units": int(r.units),
        }
        for r in rows
    ]

    return DailySalesByProductResponse(
        message="Daily sales by product fetched successfully",
        data=items,
    )


@router.get("/weekly-sales", response_model=WeeklySalesResponse)
def weekly_sales(db: Session = Depends(get_db)):
    service = AnalyticsGraphics(db)
    rows = service.get_weekly_sales()

    items = [
        {
            "week": r.week,
            "units_sold": int(r.units_sold),
            "revenue": float(r.revenue),
        }
        for r in rows
    ]

    return WeeklySalesResponse(
        message="Weekly sales fetched successfully",
        data=items,
    )


@router.get("/weekly-sales/average", response_model=WeeklySalesAverageResponse)
def weekly_sales_average(db: Session = Depends(get_db)):
    service = AnalyticsGraphics(db)
    avg = service.get_weekly_sales_average()

    if not avg:
        return WeeklySalesAverageResponse(
            message="No weekly sales data",
            data=None,
        )

    return WeeklySalesAverageResponse(
        message="Weekly sales average fetched successfully",
        data=avg,
    )