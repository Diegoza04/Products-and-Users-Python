from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.core.serializers import serialize_product
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository | None = None):
        self.product_repository = product_repository or ProductRepository()

    def list_products(self, db: Session) -> list[dict]:
        return [serialize_product(product) for product in self.product_repository.list_products(db)]

    def create_product(self, db: Session, payload: dict) -> dict:
        product = self.product_repository.create(db, **payload)
        return serialize_product(product)

    def update_product(self, db: Session, product_id: str, payload: dict) -> dict:
        product = self.product_repository.get_by_id(db, product_id)
        if not product:
            raise NotFoundError("Producto no encontrado")
        updated = self.product_repository.update(db, product, **payload)
        return serialize_product(updated)

    def delete_product(self, db: Session, product_id: str) -> dict:
        product = self.product_repository.get_by_id(db, product_id)
        if not product:
            raise NotFoundError("Producto no encontrado")
        self.product_repository.delete(db, product)
        return {"message": "Producto eliminado"}