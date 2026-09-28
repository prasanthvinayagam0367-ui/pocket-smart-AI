import base64
import hashlib
import hmac
import secrets
import jwt
from datetime import datetime, timedelta, timezone
from .config import settings

ALGORITHM = "HS256"
TOKEN_MINUTES = 60 * 24

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)
    return f"pbkdf2_sha256$120000${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}"

def verify_password(password: str, stored: str) -> bool:
    try:
        _, rounds, salt_b64, digest_b64 = stored.split("$", 3)
        salt = base64.urlsafe_b64decode(salt_b64.encode())
        expected = base64.urlsafe_b64decode(digest_b64.encode())
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(rounds))
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False

def create_token(user_id: int, username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": str(user_id), "username": username, "iat": now, "exp": now + timedelta(minutes=TOKEN_MINUTES)}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
