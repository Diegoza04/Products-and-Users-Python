from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.schemas.user import AdminUserCreate, UserRoleUpdate
from app.services.admin_service import AdminService


router = APIRouter(prefix="/api/admin", tags=["admin"])
admin_service = AdminService()


@router.get("/users")
def list_users(db: Session = Depends(get_db), _current_user: dict = Depends(require_admin)):
    return admin_service.list_users(db)


@router.post("/users")
def create_user(
    payload: AdminUserCreate,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(require_admin),
):
    return admin_service.create_user(db, payload.username, payload.password, payload.role)


@router.put("/users/{user_id}")
def update_user_role(
    user_id: str,
    payload: UserRoleUpdate,
    db: Session = Depends(get_db),
    _current_user: dict = Depends(require_admin),
):
    return admin_service.update_user_role(db, user_id, payload.role)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    return admin_service.delete_user(db, current_user["id"], user_id)


@router.get("/orders")
def list_orders(_current_user: dict = Depends(require_admin)):
    return []


@router.get("/orders/{status}")
def list_orders_by_status(status: str, _current_user: dict = Depends(require_admin)):
    return []