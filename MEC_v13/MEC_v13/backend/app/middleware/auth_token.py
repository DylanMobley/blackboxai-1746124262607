import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from config.security_policy import JWT_SECRET
from middleware.roles import has_permission
from middleware.blacklist import is_token_blacklisted

def verify_token(token: str) -> dict:
    """
    Decodes JWT, validates it, and checks against blacklist.
    Returns payload dict or None if invalid or blacklisted.
    """
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

        if is_token_blacklisted(token):
            return None

        return decoded
    except ExpiredSignatureError:
        return None
    except InvalidTokenError:
        return None

def require_auth_token(headers: dict) -> dict:
    """
    Extracts Authorization: Bearer token from headers, validates it.
    Returns decoded user info or None if invalid.
    """
    auth_header = headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]
    return verify_token(token)

def require_role(headers: dict, required_permission: str) -> bool:
    """
    Checks if the user tied to the token has the required permission.
    Returns True or False.
    """
    user = require_auth_token(headers)
    if not user:
        return False

    role = user.get("role", "guest")
    return has_permission(role, required_permission)
