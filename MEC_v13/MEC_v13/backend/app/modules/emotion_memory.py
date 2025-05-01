import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

import aioredis

logger = logging.getLogger("EmotionMemory")

REDIS_URL = "redis://localhost:6379"
EMOTION_MEMORY_KEY_PREFIX = "emotion_memory:user:"

class EmotionMemory:
    def __init__(self, redis_url: str = REDIS_URL):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)
        logger.info("Connected to Redis for EmotionMemory")

    async def close(self):
        if self.redis:
            await self.redis.close()
            logger.info("Closed Redis connection for EmotionMemory")

    async def store_emotion_state(self, user_id: int, emotion_state: Dict[str, Any]):
        """
        Store emotion state with timestamp for a user.
        """
        key = f"{EMOTION_MEMORY_KEY_PREFIX}{user_id}"
        timestamp = datetime.utcnow().isoformat()
        entry = {
            "timestamp": timestamp,
            "emotion_state": emotion_state
        }
        await self.redis.rpush(key, str(entry))
        logger.info(f"Stored emotion state for user {user_id} at {timestamp}")

    async def get_emotion_trajectory(self, user_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve the latest emotion states for a user up to the limit.
        """
        key = f"{EMOTION_MEMORY_KEY_PREFIX}{user_id}"
        entries = await self.redis.lrange(key, -limit, -1)
        trajectory = []
        for entry in entries:
            try:
                # Evaluate string representation back to dict safely
                data = eval(entry)
                trajectory.append(data)
            except Exception as e:
                logger.warning(f"Failed to parse emotion memory entry: {e}")
        return trajectory

# Singleton instance
emotion_memory = EmotionMemory()

async def init_emotion_memory():
    await emotion_memory.connect()

async def close_emotion_memory():
    await emotion_memory.close()
