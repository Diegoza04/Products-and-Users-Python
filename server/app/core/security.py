from datetime import datetime, timedelta, timezone
import base64
import binascii
import hashlib
import hmac
import secrets

import jwt

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET


PASSWORD_ALGORITHM = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 120000


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS)
    salt_b64 = base64.urlsafe_b64encode(salt).decode("ascii")
    digest_b64 = base64.urlsafe_b64encode(digest).decode("ascii")
    return f"{PASSWORD_ALGORITHM}${PASSWORD_ITERATIONS}${salt_b64}${digest_b64}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt_b64, digest_b64 = stored_hash.split("$")
        if algorithm != PASSWORD_ALGORITHM:
            return False
        salt = base64.urlsafe_b64decode(salt_b64.encode("ascii"))
        expected = base64.urlsafe_b64decode(digest_b64.encode("ascii"))
        candidate = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(iterations),
        )
        return hmac.compare_digest(candidate, expected)
    except (ValueError, TypeError, binascii.Error):
        return False


def create_access_token(payload: dict) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_payload = {**payload, "exp": expires_at}
    return jwt.encode(token_payload, JWT_SECRET, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])