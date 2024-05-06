from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings


class Database:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def initialize(cls):
        cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
        cls.db = cls.client[settings.MONGODB_DB_NAME]
        if "game" not in await cls.db.list_collection_names():
            await cls.db.create_collection("game")
        if "questions" not in await cls.db.list_collection_names():
            await cls.db.create_collection("questions")

    @classmethod
    def close(cls):
        cls.client.close()


db = Database()
