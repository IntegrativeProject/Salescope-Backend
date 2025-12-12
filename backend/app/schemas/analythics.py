from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


class BestSellingProduct(BaseModel):
    product_id: int
    name: str
    total_sold: int


class TopProduct(BestSellingProduct):
    pass


class DailySales(BaseModel):
    day: date
    units: int


class DailySalesByProduct(BaseModel):
    product_id: int
    day: date
    units: int


class WeeklySales(BaseModel):
    week: datetime
    units_sold: int
    revenue: float


class WeeklySalesAverage(BaseModel):
    avg_units_per_week: float
    avg_revenue_per_week: float


class BestProductResponse(BaseModel):
    message: str
    data: Optional[BestSellingProduct] = None


class TopProductsResponse(BaseModel):
    message: str
    data: List[TopProduct]


class DailySalesResponse(BaseModel):
    message: str
    data: List[DailySales]


class DailySalesByProductResponse(BaseModel):
    message: str
    data: List[DailySalesByProduct]


class WeeklySalesResponse(BaseModel):
    message: str
    data: List[WeeklySales]


class WeeklySalesAverageResponse(BaseModel):
    message: str
    data: Optional[WeeklySalesAverage] = None