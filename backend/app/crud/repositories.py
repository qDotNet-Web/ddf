from pydantic import ValidationError

from ..models.game_model import *
from ..core.exceptions import *
from ..core.database import db
from ..core.utils import get_uuid, get_lobby_id
from typing import List

__all__ = ["GameRepository", "PlayerRepository", "QuestionRepository"]

from ..models.game_model import QuestionRead


class GameRepository:
    @staticmethod
    def get_collection():
        return db.db["game"]

    @staticmethod
    async def gen_unique_code():
        while True:
            code = get_lobby_id()
            if not await db.exists("game", "code", code):
                return code

    @staticmethod
    async def get_by_id(lobby_id: str) -> LobbyRead:
        document = await GameRepository.get_collection().find_one({"_id": lobby_id})
        if not document:
            raise NotFoundException("Lobby nicht gefunden")
        return LobbyRead(**document)

    @staticmethod
    async def get_by_code(code: str) -> LobbyRead:
        document = await GameRepository.get_collection().find_one({"code": code})
        if not document:
            raise NotFoundException("Lobby nicht gefunden")
        return LobbyRead(**document)

    @staticmethod
    async def list() -> List[LobbyRead]:
        cursor = GameRepository.get_collection().find()
        return [LobbyRead(**document) for document in await cursor.to_list(length=None)]

    @staticmethod
    async def create(create: LobbyCreate) -> LobbyRead:
        document = create.dict()
        document["_id"] = get_uuid()
        document["code"] = await GameRepository.gen_unique_code()
        result = await GameRepository.get_collection().insert_one(document)
        assert result.acknowledged
        return await GameRepository.get_by_id(str(result.inserted_id))

    @staticmethod
    async def update(lobby_id: str, update: LobbyUpdate) -> None:
        document = update.dict(exclude_unset=True)
        result = await GameRepository.get_collection().update_one({"_id": lobby_id}, {"$set": document})
        if not result.modified_count:
            raise NotFoundException("Lobby nicht gefunden")

    @staticmethod
    async def delete(lobby_id: str) -> None:
        result = await GameRepository.get_collection().delete_one({"_id": lobby_id})
        if not result.deleted_count:
            raise NotFoundException("Lobby nicht gefunden")


class PlayerRepository:
    @staticmethod
    async def get(player_id: str) -> PlayerRead:
        document = await GameRepository.get_collection().find_one({"_id": player_id})
        if not document:
            raise NotFoundException("Spieler nicht gefunden")
        return PlayerRead(**document)

    @staticmethod
    async def list() -> List[PlayerRead]:
        cursor = GameRepository.get_collection().find()
        return [PlayerRead(**document) for document in await cursor.to_list(length=None)]

    @staticmethod
    async def create(create: PlayerCreate) -> PlayerRead:
        document = create.dict()
        document["_id"] = get_uuid()
        result = await GameRepository.get_collection().insert_one(document)
        assert result.acknowledged
        return await PlayerRepository.get(str(result.inserted_id))

    @staticmethod
    async def update(player_id: str, update: PlayerUpdate) -> None:
        document = update.dict(exclude_unset=True)
        result = await GameRepository.get_collection().update_one({"_id": player_id}, {"$set": document})
        if not result.modified_count:
            raise NotFoundException("Spieler nicht gefunden")

    @staticmethod
    async def delete(player_id: str) -> None:
        result = await GameRepository.get_collection().delete_one({"_id": player_id})
        if not result.deleted_count:
            raise NotFoundException("Spieler nicht gefunden")


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
