# backend/services/token_refresh.py

import jwt
import datetime
from config.security_policy import JWT_SECRET

def generate_new_token(payload: dict, expiry_minutes: int = 60) -> str:
    """
    Generate a new JWT token.
    :param payload: dict with user info
    :param expiry_minutes: expiration window
    :return: JWT token string
    """
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiry_minutes)
    payload.update({"exp": expiration})
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

def refresh_token(old_token: str) -> str:
    """
    Attempt to refresh an old token.
    Validates signature first (ignore expiry during validation).
    """
    try:
        decoded = jwt.decode(old_token, JWT_SECRET, algorithms=["HS256"], options={"verify_exp": False})
        new_token = generate_new_token(decoded)
        return new_token
    except Exception:
        return None
