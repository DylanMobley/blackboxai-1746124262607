import os
import re

# ─────────────────────────────────────
# 🔐 API Key Auth (legacy)
# ─────────────────────────────────────
CLONE_API_KEY = os.getenv("CLONE_API_KEY", "supersecurekey")

# ─────────────────────────────────────
# 🔐 JWT Token Secret (modern auth)
# ─────────────────────────────────────
JWT_SECRET = os.getenv("JWT_SECRET", "changeme-super-secret")

# ─────────────────────────────────────
# 🌍 CORS Whitelisting
# ─────────────────────────────────────
ALLOWED_ORIGINS = [
    "https://www.empathyethicist.ai",
    "https://api.empathyethicist.ai",
    "http://localhost:5173"
]

# ─────────────────────────────────────
# 📏 Input Constraints
# ─────────────────────────────────────
MAX_TEXT_LENGTH = 500
MAX_AUDIO_MB = 10
MAX_IMAGE_MB = 5

# ─────────────────────────────────────
# 🧪 Emotion Validation (New Freedom Mode)
# ─────────────────────────────────────
EMOTION_PATTERN = re.compile(r"^\[.*\]$")  # Allow any [something]

def is_valid_emotion(emotion: str) -> bool:
    return bool(EMOTION_PATTERN.match(emotion))

# ─────────────────────────────────────
# 🧼 File Retention (hours)
# ─────────────────────────────────────
VIDEO_RETENTION_HOURS = 12
AUDIO_RETENTION_HOURS = 12

# ─────────────────────────────────────
# 🧪 Feature Flags (optional)
# ─────────────────────────────────────
ENABLE_AUTH = True
ENABLE_USER_QUOTAS = False
ENABLE_EMOTION_FILTER = False  # Fully unlocked now
