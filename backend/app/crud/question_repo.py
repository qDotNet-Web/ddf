from pydantic import ValidationError
from ..models.game_model import QuestionRead
from ..core.exceptions import *
from ..core.database import db
from typing import List
from ..models.game_model import LobbyQuestions

__all__ = ["QuestionRepository", "RedisLobbyQuestionRepository"]


class QuestionRepository:
    @staticmethod
    async def get_collection():
        return db.db["questions"]

    @staticmethod
    async def list() -> List[QuestionRead]:
        collection = await QuestionRepository.get_collection()
        document = collection.find()
        if not document:
            raise NotFoundException("Keine Fragen gefunden")
        try:
            return [QuestionRead(**document) for document in await document.to_list(length=None)]
        except ValidationError as e:
            raise ValueError(f"Missing required fields in the database document: {e}")

    @staticmethod
    async def get_random() -> QuestionRead:
        collection = await QuestionRepository.get_collection()
        document = await collection.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
        if not document or not document[0]:
            raise NotFoundException("Keine Fragen gefunden")
        question_data = document[0]
        try:
            return QuestionRead(**question_data)
        except ValidationError as e:
            raise ValueError(f"Missing required fields in the database document: {e}")


class RedisLobbyQuestionRepository:
    @classmethod
    async def store_question(cls, lobby_questions: LobbyQuestions) -> None:
        key = f"lobby:{lobby_questions}:questions"
        await redis_client.set(key, lobby_questions.json())
        print(f"Stored lobby questions for {lobby_questions.lobby_id} in redis: {key}")

    @classmethod
    async def get_question(cls, lobby_id: str) -> LobbyQuestions:
        key = f"lobby:{lobby_id}:questions"
        data = await redis_client.get(key)
        if not data:
            raise NotFoundException(f"No questions found for lobby {lobby_id}")
        return LobbyQuestions(**data)