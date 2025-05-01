# scripts/validate_env.py

import os
import logging
from pydantic import BaseModel, validator, ValidationError, AnyUrl
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EnvValidator")

class Settings(BaseModel):
    ASYNC_DATABASE_URL: AnyUrl
    REDIS_URL: AnyUrl
    JWT_SECRET: str
    ENABLE_AUTH: bool
    ENABLE_METRICS: bool
    ZMQ_ADDRESS: str
    ZMQ_TIMEOUT_MS: int
    ZMQ_POOL_SIZE: int
    LLM_API_KEY: str
    LLM_MODEL: str
    ENABLE_RECOVERY: bool
    ENABLE_EMOTION_CACHE: bool

    @validator("JWT_SECRET", "LLM_API_KEY")
    def not_empty(cls, v):
        if not v or v.strip() == "" or "replace_this" in v:
            raise ValueError("Required value is empty or insecure")
        return v

try:
    settings = Settings(**os.environ)
    logger.info("✅ All required .env variables are valid.")
except ValidationError as e:
    logger.error("❌ Invalid environment configuration:")
    for error in e.errors():
        logger.error(f" - {error['loc'][0]}: {error['msg']}")
    exit(1)
