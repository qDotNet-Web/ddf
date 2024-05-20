import redis.asyncio as redis
from ..core.config import settings


"""redis_host = settings.REDIS_HOST
redis_port = settings.REDIS_PORT
redis_password = settings.REDIS_PASSWORD
redis_user = settings.REDIS_USER
redis_db = settings.REDIS_DB

redis_url = f"redis://{redis_user}:{redis_password}@{redis_host}:{redis_port}/{redis_db}"


class RedisClient:
    def __init__(self):
        self.client = None

    async def initialize(self):
        self.client = await redis.from_url(redis_url, encoding="utf-8", decode_responses=True)

    async def close(self):
        await self.client.close()

    def __getattr__(self, name):
        if self.client:
            return getattr(self.client, name)
        raise AttributeError("Redis client: object has no attribute {name}")


redis_client = RedisClient()
"""