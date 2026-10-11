from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate


def list_products(db: Session):
    return db.query(Product).order_by(Product.product_name).all()


def create_product(db: Session, data: ProductCreate):
    if not db.query(Category).filter(Category.id == data.category_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def update_product(db: Session, product_id: int, data: ProductCreate):
    product = get_product(db, product_id)
    if not db.query(Category).filter(Category.id == data.category_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    for key, value in data.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()
