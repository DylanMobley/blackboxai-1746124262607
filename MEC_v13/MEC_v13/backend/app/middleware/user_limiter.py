# middleware/user_limiter.py

import os
import redis
from flask import request, jsonify
from functools import wraps
from config.security_policy import JWT_SECRET
import jwt

# ─── Redis Setup ───────────────────────────────────
REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
rdb = redis.Redis.from_url(REDIS_URL)

# ─── Constants ─────────────────────────────────────
USER_RATE_LIMIT = int(os.getenv("USER_RATE_LIMIT", 100))  # Default: 100 req/hour
WINDOW_SECONDS = 3600  # 1 hour

def extract_token(headers):
    auth_header = headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return None

def get_token_identity(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload.get("sub") or payload.get("user_id") or None
    except Exception:
        return None

def user_rate_limiter():
    """
    Flask @before_request hook style rate limiter.
    """
    token = extract_token(request.headers)
    if not token:
        return  # Skip if no token (anonymous access can still have IP rate limit)

    user_identity = get_token_identity(token)
    if not user_identity:
        return  # Skip invalid tokens (already auth middleware should reject)

    key = f"user_rate_limit:{user_identity}"
    current = rdb.get(key)

    if current is None:
        rdb.setex(key, WINDOW_SECONDS, 1)
    else:
        current = int(current)
        if current >= USER_RATE_LIMIT:
            return jsonify({"error": "Rate limit exceeded (per user)."}), 429
        else:
            rdb.incr(key)
