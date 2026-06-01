from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:
    def list_recent(self, db: Session, limit: int = 100) -> list[Message]:
        query = db.query(Message).order_by(desc(Message.created_at)).limit(limit)
        return list(reversed(query.all()))