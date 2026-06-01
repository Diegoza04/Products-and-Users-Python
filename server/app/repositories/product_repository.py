from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    def list_products(self, db: Session) -> list[Product]:
        return db.query(Product).order_by(desc(Product.created_at)).all()

    def get_by_id(self, db: Session, product_id: str) -> Product | None:
        return db.get(Product, product_id)

    def create(self, db: Session, **fields) -> Product:
        product = Product(**fields)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def update(self, db: Session, product: Product, **fields) -> Product:
        for key, value in fields.items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product

    def delete(self, db: Session, product: Product) -> None:
        db.delete(product)
        db.commit()