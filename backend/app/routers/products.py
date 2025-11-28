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
    restore_product,
)


router = APIRouter(prefix="/products", tags=["products"])


class ProductAPI:
    def create(self, db: Session, payload: ProductCreate):
        product = create_product(db, payload)
        return {"message": "Product created successfully", "data": product}

    def get(self, db: Session, product_id: int):
        product = get_product(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product fetched successfully", "data": product}

    def list(self, db: Session, skip: int = 0, limit: int = 50):
        products = list_products(db, skip=skip, limit=limit)
        return {"message": "Products fetched successfully", "data": products}

    def update(self, db: Session, product_id: int, payload: ProductUpdate):
        product = update_product(db, product_id, payload)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product updated successfully", "data": product}

    def delete(self, db: Session, product_id: int):
        ok = delete_product(db, product_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted successfully"}

    def restore(self, db: Session, product_id: int):
        product = restore_product(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product restored successfully", "data": product}


product_api = ProductAPI()


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(payload: ProductCreate, db: Session = Depends(get_db)):
    return product_api.create(db, payload)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    return product_api.get(db, product_id)


@router.get("/", response_model=ProductsListResponse)
def list_products_endpoint(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return product_api.list(db, skip=skip, limit=limit)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    return product_api.update(db, product_id, payload)


@router.delete("/{product_id}", response_model=MessageResponse)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    return product_api.delete(db, product_id)


@router.put("/{product_id}/restore", response_model=ProductResponse)
def restore_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    return product_api.restore(db, product_id)
