from ..models.game_model import *
from ..core.exceptions import *
from ..core.database import db
from ..core.utils import get_uuid, get_lobby_id
from typing import List

__all__ = ["GameRepository", "PlayerRepository", "QuestionRepository"]


class GameRepository:
    @staticmethod
    def get_collection():
        return db.db["game"]

    @staticmethod
    async def get(lobby_id: str) -> LobbyRead:
        document = await GameRepository.get_collection().find_one({"_id": lobby_id})
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
        document["code"] = get_lobby_id()
        result = await GameRepository.get_collection().insert_one(document)
        assert result.acknowledged
        return await GameRepository.get(str(result.inserted_id))

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
        cursor = QuestionRepository.get_collection().find()
        return [QuestionRead(**document) for document in await cursor.to_list(length=None)]

    @staticmethod
    async def get_random() -> QuestionRead:
        document = await QuestionRepository.get_collection().aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
        if not document:
            raise NotFoundException("Keine Fragen gefunden")
        return QuestionRead(**document[0])
