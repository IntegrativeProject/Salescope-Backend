from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
    users,
    products,
    orders,
    order_items,
    auth,
    analythics,
    export_users_csv,
    export_products_csv,
    export_orders_csv,
    export_orders_items_cs,
    export_orders_detailed_csv,
    export_audit_logs_csv,
)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(order_items.router)
app.include_router(auth.router)
app.include_router(analythics.router)
app.include_router(export_users_csv.router)
app.include_router(export_products_csv.router)
app.include_router(export_orders_csv.router)
app.include_router(export_orders_items_cs.router)
app.include_router(export_orders_detailed_csv.router)
app.include_router(export_audit_logs_csv.router)

@app.get("/")
def root():
    return {"message": "SaleScope API running"}
