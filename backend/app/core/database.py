from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings



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

    @classmethod
    async def get_all_questions(cls):
        cursor = cls.db["questions"].find({})
        all_questions = await cursor.to_list(length=None)
        questions = [(question["question"], all_questions["answer"]) for question in all_questions]
        return questions


db = Database()
