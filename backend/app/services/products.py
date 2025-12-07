from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.products import Product
from ..schemas.products import ProductCreate, ProductUpdate


def create_product(db: Session, data: ProductCreate) -> Product:
    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        category=data.category,
        stock=data.stock,
        is_active=True
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, product_id: int) -> Optional[Product]:
    return (
        db.query(
            Product.product_id,
            Product.name,
            Product.description,
            Product.price,
            Product.stock,
            Product.category,
            Product.created_at,
            Product.updated_at
        )
        .filter(Product.product_id == product_id, Product.is_active == True)
        .first()
    )


def list_products(db: Session, skip: int = 0, limit: int = 50) -> List[Product]:
    return (
        db.query(
            Product.product_id,
            Product.name,
            Product.description,
            Product.price,
            Product.stock,
            Product.category,
            Product.created_at,
            Product.updated_at
        )
        .filter(Product.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_product(db: Session, product_id: int, data: ProductUpdate) -> Optional[Product]:
    product = get_product(db, product_id)
    if not product:
        return None

    if data.name is not None:
        product.name = data.name
    if data.description is not None:
        product.description = data.description
    if data.price is not None:
        product.price = data.price
    if data.stock is not None:
        product.stock = data.stock

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    product = get_product(db, product_id)
    if not product:
        return False
    product.is_active = False
    product.deleted_at = func.now()
    # product.deleted_by can be set from auth context later
    db.add(product)
    db.commit()
    db.refresh(product)
    return True


def restore_product(db: Session, product_id: int) -> Optional[Product]:
    # Query without soft-delete filters to allow restoring
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        return None
    product.is_active = True
    product.deleted_at = None
    product.deleted_by = None
    db.add(product)
    db.commit()
    db.refresh(product)
    return product