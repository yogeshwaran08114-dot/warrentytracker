from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.product import Product
from app.schemas.category import CategoryCreate


def list_categories(db: Session):
    return db.query(Category).order_by(Category.name).all()


def create_category(db: Session, data: CategoryCreate):
    if db.query(Category).filter(Category.name == data.name).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category_id: int, data: CategoryCreate):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    duplicate = db.query(Category).filter(Category.name == data.name, Category.id != category_id).first()
    if duplicate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")
    category.name = data.name
    category.description = data.description
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    if db.query(Product).filter(Product.category_id == category_id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category has products")
    db.delete(category)
    db.commit()
