"""
Redis 缓存客户端
"""

from typing import Optional, Any
import json
import redis.asyncio as aioredis

from ...utils.config import settings
from ...utils.logger import setup_logger


logger = setup_logger(__name__)


class RedisClient:
    """Redis 异步客户端封装"""

    def __init__(self):
        """初始化 Redis 客户端"""
        self.client: Optional[aioredis.Redis] = None

    async def connect(self):
        """建立连接"""
        self.client = await aioredis.from_url(
            settings.REDIS_URL,
            max_connections=settings.REDIS_MAX_CONNECTIONS,
            encoding="utf-8",
            decode_responses=True
        )
        logger.info(f"Redis 连接成功: {settings.REDIS_URL}")

    async def close(self):
        """关闭连接"""
        if self.client:
            await self.client.close()
            logger.info("Redis 连接已关闭")

    async def get(self, key: str) -> Optional[str]:
        """
        获取缓存值

        Args:
            key: 缓存键

        Returns:
            缓存值（字符串）
        """
        if not self.client:
            await self.connect()

        try:
            return await self.client.get(key)
        except Exception as e:
            logger.error(f"Redis GET 失败 [{key}]: {e}")
            return None

    async def set(
        self,
        key: str,
        value: str,
        expire: Optional[int] = None
    ) -> bool:
        """
        设置缓存值

        Args:
            key: 缓存键
            value: 缓存值
            expire: 过期时间（秒）

        Returns:
            是否成功
        """
        if not self.client:
            await self.connect()

        try:
            await self.client.set(key, value, ex=expire)
            return True
        except Exception as e:
            logger.error(f"Redis SET 失败 [{key}]: {e}")
            return False

    async def get_json(self, key: str) -> Optional[Any]:
        """
        获取 JSON 缓存

        Args:
            key: 缓存键

        Returns:
            解析后的 Python 对象
        """
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                logger.error(f"JSON 解析失败 [{key}]: {e}")
                return None
        return None

    async def set_json(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """
        设置 JSON 缓存

        Args:
            key: 缓存键
            value: Python 对象
            expire: 过期时间（秒）

        Returns:
            是否成功
        """
        try:
            json_str = json.dumps(value, ensure_ascii=False)
            return await self.set(key, json_str, expire)
        except Exception as e:
            logger.error(f"JSON 序列化失败 [{key}]: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """
        删除缓存

        Args:
            key: 缓存键

        Returns:
            是否成功
        """
        if not self.client:
            await self.connect()

        try:
            await self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis DELETE 失败 [{key}]: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """
        检查键是否存在

        Args:
            key: 缓存键

        Returns:
            是否存在
        """
        if not self.client:
            await self.connect()

        try:
            return await self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Redis EXISTS 失败 [{key}]: {e}")
            return False


# 全局 Redis 客户端实例
redis_client = RedisClient()
