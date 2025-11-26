from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, products

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

@app.get("/")
def root():
    return {"message": "SaleScope API running"}
