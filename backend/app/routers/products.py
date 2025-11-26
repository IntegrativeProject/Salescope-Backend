from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.products import (
    ProductCreate,
    ProductUpdate,
    ProductRead,
    ProductResponse,
    ProductsListResponse,
    MessageResponse,
)
from ..services.products import (
    create_product,
    get_product,
    list_products,
    update_product,
    delete_product,
)


router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(payload: ProductCreate, db: Session = Depends(get_db)):
    product = create_product(db, payload)
    return {"message": "Product created successfully", "data": product}


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product fetched successfully", "data": product}


@router.get("/", response_model=ProductsListResponse)
def list_products_endpoint(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    products = list_products(db, skip=skip, limit=limit)
    return {"message": "Products fetched successfully", "data": products}


@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product(db, product_id, payload)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully", "data": product}


@router.delete("/{product_id}", response_model=MessageResponse)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    ok = delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

