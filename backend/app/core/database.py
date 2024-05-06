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
        if "accounts" not in await cls.db.list_collection_names():
            await cls.db.create_collection("accounts")

    @classmethod
    def close(cls):
        cls.client.close()

    @classmethod
    async def exists(cls, collection_name: str, field: str, value) -> bool:
        """
        Prüft, ob ein bestimmter Wert in einer angegebenen Collection vorhanden ist.
        :param collection_name: Der Name der MongoDB-Collection.
        :param field: Das zu prüfende Feld.
        :param value: Der gesuchte Wert.
        :return: True, wenn der Wert vorhanden ist, ansonsten False.
        """
        if cls.db is None:
            raise ValueError("Database not initialized")
        collection = cls.db[collection_name]
        document = await collection.find_one({field: value})
        return document is not None


db = Database()
