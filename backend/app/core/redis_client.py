import redis.asyncio as redis
from ..core.config import settings


redis_host = settings.REDIS_HOST
redis_port = settings.REDIS_PORT
redis_password = settings.REDIS_PASSWORD
redis_user = settings.REDIS_USER
redis_db = settings.REDIS_DB

redis_url = f"redis://{redis_user}:{redis_password}@{redis_host}:{redis_port}/{redis_db}"


class RedisClient:
    def __init__(self):
        self.client = None

    async def initialize(self):
        self.client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)

    def close(self):
        self.client.close()


redis_client = RedisClient()
