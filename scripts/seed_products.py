from app.core.database import init_db
from app.core.deps import SessionLocal
from app.models.category import Category
from app.models.product import Product


SAMPLE_PRODUCTS = [
    {
        "category": "Laptops",
        "category_description": "Portable computers for work, study, and gaming.",
        "product_name": "Dell Inspiron 15 Laptop",
        "brand": "Dell",
        "model_number": "Inspiron 15 3530",
        "default_warranty_months": 12,
    },
    {
        "category": "Laptops",
        "category_description": "Portable computers for work, study, and gaming.",
        "product_name": "HP Victus 15 Gaming Laptop",
        "brand": "HP",
        "model_number": "Victus 15-fa2701TX",
        "default_warranty_months": 12,
    },
    {
        "category": "Laptops",
        "category_description": "Portable computers for work, study, and gaming.",
        "product_name": "Lenovo IdeaPad Slim 5",
        "brand": "Lenovo",
        "model_number": "IdeaPad Slim 5 14IRL8",
        "default_warranty_months": 12,
    },
    {
        "category": "Smartphones",
        "category_description": "Mobile phones and accessories.",
        "product_name": "Samsung Galaxy S25",
        "brand": "Samsung",
        "model_number": "SM-S931B",
        "default_warranty_months": 12,
    },
    {
        "category": "Smartphones",
        "category_description": "Mobile phones and accessories.",
        "product_name": "Apple iPhone 16",
        "brand": "Apple",
        "model_number": "A3287",
        "default_warranty_months": 12,
    },
    {
        "category": "Smartphones",
        "category_description": "Mobile phones and accessories.",
        "product_name": "OnePlus 13",
        "brand": "OnePlus",
        "model_number": "CPH2653",
        "default_warranty_months": 12,
    },
    {
        "category": "Audio",
        "category_description": "Headphones, earbuds, and home audio equipment.",
        "product_name": "Sony WH-1000XM5 Headphones",
        "brand": "Sony",
        "model_number": "WH1000XM5/B",
        "default_warranty_months": 24,
    },
    {
        "category": "Televisions",
        "category_description": "Smart televisions and home entertainment displays.",
        "product_name": "Samsung 55-inch 4K Smart TV",
        "brand": "Samsung",
        "model_number": "UA55DU8000KXXL",
        "default_warranty_months": 24,
    },
    {
        "category": "Home Appliances",
        "category_description": "Cooling and everyday household appliances.",
        "product_name": "LG 1.5 Ton Split AC",
        "brand": "LG",
        "model_number": "PS-Q19CNXE",
        "default_warranty_months": 12,
    },
    {
        "category": "Cameras",
        "category_description": "Digital cameras and photography equipment.",
        "product_name": "Canon EOS R50 Camera",
        "brand": "Canon",
        "model_number": "EOS R50 RF-S18-45",
        "default_warranty_months": 12,
    },
]


def seed_products() -> int:
    init_db()
    db = SessionLocal()
    created = 0
    try:
        for item in SAMPLE_PRODUCTS:
            category = db.query(Category).filter(Category.name == item["category"]).first()
            if category is None:
                category = Category(
                    name=item["category"],
                    description=item["category_description"],
                )
                db.add(category)
                db.flush()

            existing = db.query(Product).filter(
                Product.model_number == item["model_number"]
            ).first()
            if existing is not None:
                continue

            db.add(Product(
                product_name=item["product_name"],
                brand=item["brand"],
                model_number=item["model_number"],
                category_id=category.id,
                default_warranty_months=item["default_warranty_months"],
            ))
            created += 1

        db.commit()
        return created
    finally:
        db.close()


if __name__ == "__main__":
    print(f"Added {seed_products()} sample products.")
