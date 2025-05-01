# middleware/blacklist.py

import threading
import time

# In-memory store (Redis optional upgrade later)
_blacklisted_tokens = {}
_lock = threading.Lock()

# Default blacklist expiration time (seconds)
BLACKLIST_EXPIRATION_SECONDS = 3600  # 1 hour

def blacklist_token(token: str, expiry_seconds: int = BLACKLIST_EXPIRATION_SECONDS):
    """
    Add a token to the blacklist with optional expiry time.
    """
    with _lock:
        expire_at = time.time() + expiry_seconds
        _blacklisted_tokens[token] = expire_at

def is_token_blacklisted(token: str) -> bool:
    """
    Check if a token is currently blacklisted.
    Also purges expired entries.
    """
    with _lock:
        now = time.time()
        expired_tokens = [t for t, exp in _blacklisted_tokens.items() if exp < now]
        for t in expired_tokens:
            del _blacklisted_tokens[t]

        return token in _blacklisted_tokens
