from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings


class Database:
    client: AsyncIOMotorClient = None

    @classmethod
    async def initialize(cls):
        cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
        cls.db = cls.client[settings.MONGODB_DB_NAME]
        if "users" not in await cls.db.list_collection_names():
            await cls.db.create_collection("users")
        if "games" not in await cls.db.list_collection_names():
            await cls.db.create_collection("games")

    @classmethod
    def close(cls):
        cls.client.close()


db = Database()
