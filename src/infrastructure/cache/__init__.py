"""
缓存模块
"""

from .redis_client import RedisClient, redis_client

__all__ = ["RedisClient", "redis_client"]
