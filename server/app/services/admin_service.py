from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError, ValidationError
from app.core.security import hash_password
from app.core.serializers import serialize_user
from app.repositories.user_repository import UserRepository


class AdminService:
    def __init__(self, user_repository: UserRepository | None = None):
        self.user_repository = user_repository or UserRepository()

    def list_users(self, db: Session) -> list[dict]:
        return [serialize_user(user) for user in self.user_repository.list_users(db)]

    def create_user(self, db: Session, username: str, password: str, role: str = "user") -> dict:
        normalized_username = username.strip()

        if not normalized_username or not password:
            raise ValidationError("username y password son obligatorios")
        if role not in {"user", "admin"}:
            raise ValidationError("Rol invalido")
        if self.user_repository.get_by_username(db, normalized_username):
            raise ConflictError("El usuario ya existe")

        user = self.user_repository.create(
            db,
            username=normalized_username,
            password_hash=hash_password(password),
            role=role,
        )
        return serialize_user(user)

    def update_user_role(self, db: Session, user_id: str, role: str) -> dict:
        if role not in {"user", "admin"}:
            raise ValidationError("Rol invalido")
        user = self.user_repository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("Usuario no encontrado")
        updated = self.user_repository.update_role(db, user, role)
        return serialize_user(updated)

    def delete_user(self, db: Session, current_user_id: str, user_id: str) -> dict:
        if str(current_user_id) == str(user_id):
            raise ForbiddenError("No puedes eliminarte a ti mismo")
        user = self.user_repository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("Usuario no encontrado")
        self.user_repository.delete(db, user)
        return {"message": "Usuario eliminado"}