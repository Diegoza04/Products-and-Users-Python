from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError, UnauthorizedError, ValidationError
from app.core.security import create_access_token, hash_password, verify_password
from app.core.serializers import serialize_user
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository | None = None):
        self.user_repository = user_repository or UserRepository()

    def register(self, db: Session, username: str, password: str, role: str = "user") -> dict:
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

    def login(self, db: Session, username: str, password: str) -> dict:
        user = self.user_repository.get_by_username(db, username.strip())
        if not user:
            raise NotFoundError("Usuario no encontrado")
        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Contrasena incorrecta")

        token = create_access_token({"id": user.id, "username": user.username, "role": user.role})
        return {"token": token}