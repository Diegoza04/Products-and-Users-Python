from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService


router = APIRouter(prefix="/api/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register(db, payload.username, payload.password, payload.role)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(db, payload.username, payload.password)