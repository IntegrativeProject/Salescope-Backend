from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from ..models.products import Product
from ..schemas.products import ProductCreate, ProductUpdate, ProductRead as ProductSchema


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
    return db.query(Product).filter(
        Product.product_id == product_id,
        Product.is_active == True
    ).first()


def list_products(db: Session, skip: int = 0, limit: int = 50) -> List[Product]:
    return db.query(Product).filter(
        Product.is_active == True
    ).offset(skip).limit(limit).all()


def update_product(db: Session, product_id: int, data: ProductUpdate) -> Optional[Product]:
    product = db.query(Product).filter(
        Product.product_id == product_id,
        Product.is_active == True
    ).first()
    
    if not product:
        return None
        
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
        
    product.updated_at = datetime.utcnow()
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    product = db.query(Product).filter(
        Product.product_id == product_id,
        Product.is_active == True
    ).first()
    
    if not product:
        return False
    
    product.is_active = False
    product.deleted_at = func.now()
    db.add(product)
    db.commit()
    db.refresh(product)
    return True


def restore_product(db: Session, product_id: int) -> Optional[Product]:
    product = db.query(Product).filter(
        Product.product_id == product_id,
        Product.is_active == False  
    ).first()
    
    if not product:
        return None
        
    product.is_active = True
    product.deleted_at = None
    product.deleted_by = None
    product.updated_at = datetime.utcnow()
    
    db.add(product)
    db.commit()
    db.refresh(product)
    return product