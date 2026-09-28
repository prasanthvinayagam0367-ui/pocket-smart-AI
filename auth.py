from fastapi import Depends, HTTPException, Request, status
from .db import get_db
from .security import decode_token

COOKIE_NAME = "pocketsmart_token"

def get_current_user(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.lower().startswith("bearer "):
            token = auth[7:].strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")
    with get_db() as conn:
        user = conn.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return dict(user)
