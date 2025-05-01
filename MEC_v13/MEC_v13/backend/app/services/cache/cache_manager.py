import redis
import logging
import os

# Set up a Redis connection
cache = redis.StrictRedis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0, decode_responses=True)

# Set up logging for cache operations
logger = logging.getLogger("CacheManager")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("logs/cache_manager.log")
fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(fh)

def set_cache(key: str, value: str, ttl: int = 3600, user_activity_level: str = "high"):
    """
    Set a cache value with TTL dynamically based on key type and user activity.

    Args:
        key (str): The cache key.
        value (str): The value to store in the cache.
        ttl (int, optional): Default TTL in seconds. Defaults to 3600 seconds (1 hour).
        user_activity_level (str, optional): User's activity level (e.g., "high", "low").
    """
    # Dynamically adjust TTL based on user activity level and key type
    if user_activity_level == "high":
        ttl = ttl // 2  # Shorten TTL for active users
    elif user_activity_level == "low":
        ttl = ttl * 2  # Extend TTL for less active users

    # Apply type-based dynamic TTL
    if "persona" in key:
        ttl = 600  # 10 minutes for persona-related data
    elif "emotion" in key:
        ttl = 300  # 5 minutes for emotion-related data
    elif "symbolic" in key:
        ttl = 120  # 2 minutes for symbolic engine responses

    try:
        cache.setex(key, ttl, value)
        logger.info(f"Cache set for key: {key}, TTL: {ttl}s")
    except Exception as e:
        logger.error(f"Error setting cache for key {key}: {e}")

def get_cache(key: str):
    """
    Retrieve a cache value. Returns None if expired or not found.

    Args:
        key (str): The cache key.

    Returns:
        str or None: The cached value or None if not found/expired.
    """
    try:
        value = cache.get(key)
        if value is None:
            logger.info(f"Cache miss for key: {key}")
        else:
            logger.info(f"Cache hit for key: {key}")
        return value
    except Exception as e:
        logger.error(f"Error retrieving cache for key {key}: {e}")
        return None

def delete_cache(key: str):
    """
    Remove a cache key from Redis.

    Args:
        key (str): The cache key to delete.
    """
    try:
        cache.delete(key)
        logger.info(f"Cache deleted for key: {key}")
    except Exception as e:
        logger.error(f"Error deleting cache for key {key}: {e}")

def clear_all_cache():
    """
    Clears all cache from Redis.
    """
    try:
        cache.flushdb()
        logger.info("All cache cleared.")
    except Exception as e:
        logger.error(f"Error clearing all cache: {e}")
