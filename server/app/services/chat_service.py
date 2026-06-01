from sqlalchemy.orm import Session

from app.core.serializers import serialize_message
from app.repositories.message_repository import MessageRepository


class ChatService:
    def __init__(self, message_repository: MessageRepository | None = None):
        self.message_repository = message_repository or MessageRepository()

    def history(self, db: Session) -> list[dict]:
        return [serialize_message(message) for message in self.message_repository.list_recent(db)]