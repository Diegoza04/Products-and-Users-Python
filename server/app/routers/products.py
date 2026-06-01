from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.product_service import ProductService


router = APIRouter(prefix="/api/products", tags=["products"])
product_service = ProductService()


@router.get("")
@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return product_service.list_products(db)


@router.post("")
@router.post("/")
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(require_admin),
):
    return product_service.create_product(db, payload.model_dump())


@router.put("/{product_id}")
def update_product(
    product_id: str,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(require_admin),
):
    return product_service.update_product(db, product_id, payload.model_dump())


@router.delete("/{product_id}")
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(require_admin),
):
    return product_service.delete_product(db, product_id)