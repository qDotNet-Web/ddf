from ..models.game_model import PlayerRead, PlayerCreate, PlayerUpdate
from ..core.exceptions import *
from ..core.utils import get_uuid
from ..core.database import db
from .game_repo import GameRepository
from .lobby_repo import lobby_manager
from typing import List

__all__ = ["PlayerRepository"]


class PlayerRepository:
    @staticmethod
    async def get_collection():
        return db.db["players"]

    @staticmethod
    async def get(player_id: str) -> PlayerRead:
        collection = await PlayerRepository.get_collection()
        document = await collection.find_one({"_id": player_id})
        if not document:
            raise NotFoundException("Spieler nicht gefunden")
        return PlayerRead(**document)

    @staticmethod
    async def list() -> List[PlayerRead]:
        collection = await PlayerRepository.get_collection()
        cursor = collection.find()
        return [PlayerRead(**document) for document in await cursor.to_list(length=None)]

    @staticmethod
    async def create_player(player_create: PlayerCreate) -> PlayerRead:
        """
        Create a new player
        @param player_create:
        @return:
        """
        document = player_create.dict()
        document["_id"] = get_uuid()
        result = await GameRepository.get_collection().insert_one(document)
        assert result.acknowledged
        await lobby_manager.create_player(document["_id"], document["name"], document["lobby_id"])
        return await GameRepository.get_player_by_id(str(result.inserted_id))

    @staticmethod
    async def update(player_id: str, update: PlayerUpdate) -> None:
        collection = await PlayerRepository.get_collection()
        document = update.dict(exclude_unset=True)
        result = await collection.update_one({"_id": player_id}, {"$set": document})
        if not result.modified_count:
            raise NotFoundException("Spieler nicht gefunden")

    @staticmethod
    async def delete(player_id: str) -> None:
        collection = await PlayerRepository.get_collection()
        result = await collection.delete_one({"_id": player_id})
        if not result.deleted_count:
            raise NotFoundException("Spieler nicht gefunden")
