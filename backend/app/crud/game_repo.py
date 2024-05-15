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

        @rtype: LobbyRead
        @param lobby_id:
        @return: LobbyRead
        """
        document = await GameRepository.get_collection().find_one({"_id": lobby_id})
        if not document:
            raise NotFoundException("Lobby nicht gefunden")
        return LobbyRead(**document)

    @staticmethod
    async def get_player_by_id(player_id: str) -> PlayerRead:
        document = await GameRepository.get_collection().find_one({"_id": player_id})
        if not document:
            raise NotFoundException("Spieler nicht gefunden")
        return PlayerRead(**document)

    @staticmethod
    async def get_by_code(code: str) -> LobbyRead:
        """
        Get a lobby by its code
        @rtype: LobbyRead
        @param code: str
        @return: LobbyRead
        """
        document = await GameRepository.get_collection().find_one({"code": code})
        if not document:
            raise NotFoundException("Lobby nicht gefunden")
        return LobbyRead(**document)

    @staticmethod
    async def list() -> List[LobbyRead]:
        """
        List all lobbies
        @return: List[LobbyRead]
        """
        cursor = GameRepository.get_collection().find()
        return [LobbyRead(**document) for document in await cursor.to_list(length=None)]

    @staticmethod
    async def create(create: LobbyCreate, owner_name: str, owner_avatar_id: int = None) -> LobbyRead:
        """
        Create a new lobby
        @param create: LobbyCreate
        @param owner_name:
        @param owner_avatar_id:
        @return: LobbyRead
        """
        player = PlayerCreate(name=owner_name, avatar_id=owner_avatar_id)
        player = await GameRepository.create_player(player)

        document = create.dict()
        document["_id"] = get_uuid()
        document["code"] = await GameRepository.gen_unique_code()
        document["owner_id"] = player.player_id
        document["owner_name"] = player.name

        lobby_manager.create_lobby(document["_id"], document)
        result = await GameRepository.get_collection().insert_one(document)
        assert result.acknowledged
        return await GameRepository.get_by_id(str(result.inserted_id))

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
    async def update(lobby_id: str, update: LobbyUpdate) -> None:
        """
        Update a lobby
        @param lobby_id: str
        @param update: LobbyUpdate
        """
        document = update.dict(exclude_unset=True)
        result = await GameRepository.get_collection().update_one({"_id": lobby_id}, {"$set": document})
        if not result.modified_count:
            raise NotFoundException("Lobby nicht gefunden")

    @staticmethod
    async def delete(lobby_id: str) -> None:
        """
        Delete a lobby
        @param lobby_id: str
        """
        result = await GameRepository.get_collection().delete_one({"_id": lobby_id})
        if not result.deleted_count:
            raise NotFoundException("Lobby nicht gefunden")

    @staticmethod
    async def add_player_to_lobby_by_id(lobby_id: str, player_name: str) -> LobbyRead:
        """
        Add a player to a lobby by its id
        @param lobby_id: str
        @param player_name: str
        @return: LobbyRead
        """
        result = await GameRepository.get_collection().update_one(
            {"_id": lobby_id},
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
    async def save_lobby_from_redis(lobby_id: str, lobby_data: LobbyRead) -> None:
        """
        Save a lobby from Redis to the database
        @param lobby_id: str
        @param lobby_data: LobbyRead
        """
        await GameRepository.get_collection().insert_one(lobby_data)
        await lobby_manager.delete_lobby(lobby_id)
