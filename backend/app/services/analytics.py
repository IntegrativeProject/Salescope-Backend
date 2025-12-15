from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.orders import Order
from ..models.order_item import OrderItem
from ..models.products import Product

# Only consider real sales for analytics
PAID_STATUSES = ("paid", "shipped", "pending", "cancelled", "refunded")

class AnalyticsGraphics:
    def __init__(self, db: Session) -> None:
        self.db = db

    #  1. The product want the highest total quantity sold (sum of the quantity in order_items).
    def get_best_selling_product(self):
        q = (
            self.db.query(
                Product.product_id,
                Product.name,
                func.sum(OrderItem.quantity).label("total_sold"),
            )
            .join(OrderItem, OrderItem.product_id == Product.product_id)
            .join(Order, Order.order_id == OrderItem.order_id)
            .filter(Order.status.in_(PAID_STATUSES))
            .group_by(Product.product_id, Product.name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(1)
        )
        return q.first()

    # 2. list of products with the highest sold (Top 5).
    def get_top_selling_products(self, limit: int = 5):
        q = (
            self.db.query(
                Product.product_id,
                Product.name,
                func.sum(OrderItem.quantity).label("total_sold"),
            )
            .join(OrderItem, OrderItem.product_id == Product.product_id)
            .join(Order, Order.order_id == OrderItem.order_id)
            .filter(Order.status.in_(PAID_STATUSES))
            .group_by(Product.product_id, Product.name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
        )
        return q.all()

    # 3. Days with highest solds
    def get_best_selling_days(self):
        day = func.date(Order.created_at)
        q = (
            self.db.query(
                day.label("day"),
                func.sum(OrderItem.quantity).label("total_units"),
                func.sum(OrderItem.total_price).label("total_revenue"),
            )
            .join(OrderItem, OrderItem.order_id == Order.order_id)
            .filter(Order.status.in_(PAID_STATUSES))
            .group_by(day)
            .order_by(func.sum(OrderItem.quantity).desc())
        )
        return q.all()

    # 4. average of week sales.
    def get_weekly_sales(self):
        week = func.date_trunc("week", Order.created_at)
        q = (
            self.db.query(
                week.label("week"),
                func.coalesce(func.sum(OrderItem.quantity), 0).label("units_sold"),
                func.coalesce(
                    func.sum(OrderItem.total_price),
                    func.sum(Order.total_amount),
                ).label("revenue"),
            )
            .outerjoin(OrderItem, OrderItem.order_id == Order.order_id)
            .filter(Order.status.in_(PAID_STATUSES))
            .group_by(week)
            .order_by(week.desc())
        )
        rows = q.all()
        return rows

    # 4.1 weekly average sales.
    def get_weekly_sales_average(self):
        week_sales = self.get_weekly_sales()

        if not week_sales:
            return None
        total_units = sum(r.units_sold for r in week_sales)
        total_revenue = sum(r.revenue for r in week_sales)
        n_weeks = len(week_sales)
        return {
            "avg_units_per_week": float(total_units) / n_weeks,
            "avg_revenue_per_week": float(total_revenue) / n_weeks,
        }

    # 5. total daily sales
    def get_daily_sales(self):
        day = func.date(Order.created_at)
        q = (
            self.db.query(
                day.label("day"),
                func.sum(OrderItem.quantity).label("units"),
            )
            .join(OrderItem, OrderItem.order_id == Order.order_id)
            .filter(Order.status.in_(PAID_STATUSES))
            .group_by(day)
            .order_by(day.asc())
        )
        return q.all()

    # 6. Sales per products per day
    def get_daily_sales_by_product(self):
        day = func.date(Order.created_at)
        q = (
            self.db.query(
                Product.product_id,
                day.label("day"),
                func.sum(OrderItem.quantity).label("units"),
            )
            .join(OrderItem, OrderItem.product_id == Product.product_id)
            .join(Order, Order.order_id == OrderItem.order_id)
            .filter(Order.status.in_(PAID_STATUSES))
            .group_by(Product.product_id, day)
            .order_by(Product.product_id, day)
        )
        return q.all()