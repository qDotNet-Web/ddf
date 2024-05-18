from ..models.game_model import *
from ..core.exceptions import *
from ..core.database import db
from ..core.utils import get_uuid, get_lobby_id
from .lobby_repo import lobby_manager
from typing import List

__all__ = ["GameRepository"]


class GameRepository:
    @staticmethod
    def get_collection():
        return db.db["game"]

    @staticmethod
    async def gen_unique_code():
        """
        Generate a unique code for a lobby
        @return: string
        """
        while True:
            code = get_lobby_id()
            if not await db.exists("game", "code", code):
                return code

    @staticmethod
    async def get_by_id(lobby_id: str) -> LobbyRead:
        """
        Get a lobby by its ID
        @param lobby_id: str
        @return: LobbyRead
        """
        document = await GameRepository.get_collection().find_one({"_id": str(lobby_id)})
        if not document:
            raise NotFoundException("Lobby nicht gefunden")
        document.setdefault("code", "None")
        document.setdefault("owner_name", "None")
        document.setdefault("is_active", None)
        document.setdefault("round_timer", None)
        document.setdefault("lives_per_player", None)
        document.setdefault("owner_id", None)
        document.setdefault("text_based", None)
        return LobbyRead(**document)

    @staticmethod
    async def get_by_code(code: str) -> LobbyRead:
        """
        Get a lobby by its code
        @param code: str
        @return: LobbyRead
        """
        document = await GameRepository.get_collection().find_one({"code": code})
        if not document:
            raise NotFoundException("Lobby nicht gefunden")
        document.setdefault("code", "None")
        document.setdefault("owner_name", "None")
        document.setdefault("is_active", None)
        document.setdefault("round_timer", None)
        document.setdefault("lives_per_player", None)
        document.setdefault("owner_id", None)
        document.setdefault("text_based", None)
        return LobbyRead(**document)

    @staticmethod
    async def list() -> List[LobbyRead]:
        """
        List all lobbies
        @return: List[LobbyRead]
        """
        cursor = GameRepository.get_collection().find()
        lobbies = []
        for document in await cursor.to_list(length=None):
            document.setdefault("code", "None")
            document.setdefault("owner_name", "None")
            document.setdefault("is_active", None)
            document.setdefault("round_timer", None)
            document.setdefault("lives_per_player", None)
            document.setdefault("owner_id", None)
            document.setdefault("text_based", None)
            lobbies.append(LobbyRead(**document))
        return lobbies

    @staticmethod
    async def create(create: LobbyCreate) -> LobbyRead:
        """
        Create a new lobby
        @param create: LobbyCreate
        @return: LobbyRead
        """
        document = create.dict()
        document["_id"] = get_uuid()
        document["code"] = await GameRepository.gen_unique_code()

        result = await GameRepository.get_collection().insert_one(document)
        assert result.acknowledged
        return await GameRepository.get_by_id(str(result.inserted_id))

    @staticmethod
    async def update(lobby_id: str, update: LobbyUpdate) -> None:
        """
        Update a lobby
        @param lobby_id: str
        @param update: LobbyUpdate
        """
        document = update.dict(exclude_unset=True)
        result = await GameRepository.get_collection().update_one({"_id": str(lobby_id)}, {"$set": document})
        if not result.modified_count:
            raise NotFoundException("Lobby nicht gefunden")

    @staticmethod
    async def delete(lobby_id: str) -> None:
        """
        Delete a lobby
        @param lobby_id: str
        """
        result = await GameRepository.get_collection().delete_one({"_id": str(lobby_id)})
        if not result.deleted_count:
            raise NotFoundException("Lobby nicht gefunden")

    @staticmethod
    async def add_player_to_lobby_by_id(lobby_id: str, player_name: str) -> LobbyRead:
        """
        Add a player to a lobby by its ID
        @param lobby_id: str
        @param player_name: str
        @return: LobbyRead
        """
        result = await GameRepository.get_collection().update_one(
            {"_id": str(lobby_id)},
            {"$addToSet": {"players": player_name}}
        )
        if not result.modified_count:
            raise NotFoundException("Lobby not found or player already in lobby")
        return await GameRepository.get_by_id(lobby_id)

    @staticmethod
    async def add_player_to_lobby_by_code(code: str, player_name: str) -> LobbyRead:
        """
        Add a player to a lobby by its code
        @param code: str
        @param player_name: str
        @return: LobbyRead
        """
        result = await GameRepository.get_collection().update_one(
            {"code": code},
            {"$addToSet": {"players": player_name}}
        )
        if not result.modified_count:
            raise NotFoundException("Lobby not found or player already in lobby")
        return await GameRepository.get_by_code(code)

    @staticmethod
    async def save_lobby_from_redis(lobby_id: str, lobby_data: LobbyUpdate) -> None:
        """
        Save a lobby from Redis to the database
        @param lobby_id: str
        @param lobby_data: LobbyRead
        """
        await GameRepository.get_collection().insert_one(lobby_data.dict())
        await lobby_manager.delete_lobby(lobby_id)

    @staticmethod
    async def update_player_lobby(player_id: str, lobby_id: str) -> None:
        """
        Update the lobby_id of a player
        @param player_id: str
        @param lobby_id: str
        """
        result = await GameRepository.get_collection().update_one(
            {"_id": str(player_id)},
            {"$set": {"lobby_id": lobby_id}}
        )
        if not result.modified_count:
            raise NotFoundException("Spieler nicht gefunden")
