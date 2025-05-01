# backend/middleware/auth_required.py

import functools
from flask import request, jsonify
from config.security_policy import ENABLE_AUTH
from backend.services.auth_token import require_auth_token

def auth_required(func):
    """
    Decorator to secure endpoints with optional JWT token validation.
    If ENABLE_AUTH is False, allows normal access (Freedom Mode).
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if ENABLE_AUTH:
            token_data = require_auth_token(request.headers)
            if not token_data:
                return jsonify({"error": "Unauthorized access (invalid or missing token)"}), 401
        return func(*args, **kwargs)

    return wrapper
