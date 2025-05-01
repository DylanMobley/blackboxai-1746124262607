from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config.logging_config import setup_logger
import os

# ─── Logger ───────────────────────────────────────
logger = setup_logger("RateLimiter", "logs/limiter.log")

# ─── Flask-Limiter Setup ──────────────────────────
def configure_limiter(app):
    """
    Attach rate limiter to Flask app.
    Limits are defined per IP (or future auth token).
    """
    redis_url = os.getenv("REDIS_RATE_LIMIT_URL", "redis://localhost:6379/0")

    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=["100 per hour", "10 per minute"],
        storage_uri=redis_url
    )

    @limiter.request_filter
    def internal_bypass():
        return get_remote_address() in ("127.0.0.1", "localhost")

    logger.info(f"🔒 Rate limiter initialized via Redis → {redis_url}")
    return limiter
