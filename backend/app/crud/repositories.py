from ..models.game_model import *
from ..core.exceptions import *
from ..core.database import db
from ..core.utils import get_uuid
from fastapi import HTTPException

__all__ = ["GameRepository", "PlayerRepository", "QuestionRepository"]


def get_game_collection():
    try:
        return db.db["game"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch game collection: {str(e)}")


def get_question_collection():
    try:
        return db.db["questions"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch question collection: {str(e)}")


class GameRepository:
    @staticmethod
    def get(lobby_id: str) -> LobbyRead:
        document = get_game_collection().find_one({"_id": lobby_id})
        if not document:
            raise NotFoundException("Lobby not found")
        return LobbyRead(**document)

    @staticmethod
    def list() -> LobbyRead:
        cursor = get_game_collection().find()
        return [LobbyRead(**document) for document in cursor]

    @staticmethod
    def create(create: LobbyCreate) -> LobbyRead:
        document = create.dict()
        document["_id"] = get_uuid()
        result = get_game_collection().insert_one(document)
        assert result.acknowledged
        return GameRepository.get(result.inserted_id)

    @staticmethod
    def update(lobby_id: str, update: LobbyUpdate) -> None:
        document = update.dict()
        result = get_game_collection().update_one({"_id": lobby_id}, {"$set": document})
        if not result.modified_count:
            raise NotFoundException("Lobby not found")

    @staticmethod
    def delete(lobby_id: str) -> None:
        result = get_game_collection().delete_one({"_id": lobby_id})
        if not result.deleted_count:
            raise NotFoundException("Lobby not found")


class PlayerRepository:
    @staticmethod
    def get(player_id: str) -> PlayerRead:
        document = get_game_collection().find_one({"_id": player_id})
        if not document:
            raise NotFoundException("Player not found")
        return PlayerRead(**document)

    @staticmethod
    def list() -> PlayerRead:
        cursor = get_game_collection().find()
        return [PlayerRead(**document) for document in cursor]

    @staticmethod
    def create(create: PlayerCreate) -> PlayerRead:
        document = create.dict()
        document["_id"] = get_uuid()
        result = get_game_collection().insert_one(document)
        assert result.acknowledged
        return PlayerRepository.get(result.inserted_id)

    @staticmethod
    def update(player_id: str, update: PlayerUpdate) -> None:
        document = update.dict()
        result = get_game_collection().update_one({"_id": player_id}, {"$set": document})
        if not result.modified_count:
            raise NotFoundException("Player not found")

    @staticmethod
    def delete(player_id: str) -> None:
        result = get_game_collection().delete_one({"_id": player_id})
        if not result.deleted_count:
            raise NotFoundException("Player not found")


class QuestionRepository:
    @staticmethod
    def get_random() -> QuestionRead:
        collection = get_question_collection()
        document = collection.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
        if not document:
            raise NotFoundException("No Questions found")
        return QuestionRead(**document[0])
