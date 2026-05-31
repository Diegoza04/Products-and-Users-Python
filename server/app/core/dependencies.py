from fastapi import Depends, Header

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_access_token


def require_auth(authorization: str | None = Header(default=None)) -> dict:
    if not authorization:
        raise UnauthorizedError("Falta token")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise UnauthorizedError("Falta token")

    try:
        return decode_access_token(token)
    except Exception as exc:  # noqa: BLE001
        raise ForbiddenError("Token invalido") from exc


def require_admin(current_user: dict = Depends(require_auth)) -> dict:
    if current_user.get("role") != "admin":
        raise ForbiddenError("No autorizado")
    return current_user