import jwt
from flask import request
from config.security_policy import JWT_SECRET

def require_jwt():
    def decorator(fn):
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization", "").replace("Bearer ", "")
            if not token:
                return {"error": "Missing token"}, 401
            try:
                jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
                return fn(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return {"error": "Token expired"}, 401
            except Exception as e:
                return {"error": "Invalid token"}, 403
        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator
