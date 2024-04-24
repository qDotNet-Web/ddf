from app.models import Question
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import json


async def insert_questions():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client['ddf_db']

    with open('questions.json', 'r') as file:
        questions = json.load(file)

    question_models = [Question(**question) for question in questions]
    question_dicts = [question.dict(by_alias=True) for question in question_models]

    await db.questions.insert_many(question_dicts)
    print("Fragen wurden hinzugefügt")
    await client.close()


if __name__ == "__main__":
    asyncio.run(insert_questions())