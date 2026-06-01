from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def list_users(self, db: Session) -> list[User]:
        return db.query(User).order_by(desc(User.created_at)).all()

    def get_by_id(self, db: Session, user_id: str) -> User | None:
        return db.get(User, user_id)

    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, username: str, password_hash: str, role: str) -> User:
        user = User(username=username, password_hash=password_hash, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update_role(self, db: Session, user: User, role: str) -> User:
        user.role = role
        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user: User) -> None:
        db.delete(user)
        db.commit()