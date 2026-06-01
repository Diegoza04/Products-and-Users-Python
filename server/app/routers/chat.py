from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_auth
from app.services.chat_service import ChatService


router = APIRouter(prefix="/api/chat", tags=["chat"])
chat_service = ChatService()


@router.get("/history")
def history(db: Session = Depends(get_db), _current_user: dict = Depends(require_auth)):
    return chat_service.history(db)