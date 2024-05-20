from ..models.game_model import *
from ..core.exceptions import *
from ..core.database import db
from ..core.utils import get_uuid, get_lobby_id
from .player_repo import PlayerRepository
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
        document.setdefault("game_state", None)
        document.setdefault("round_timer", None)
        document.setdefault("lives_per_player", None)
        document.setdefault("owner_id", None)
        document.setdefault("game_type", None)

        if "players" in document:
            players = []
            for player in document["players"]:
                if isinstance(player, dict):
                    players.append(Player(**player))
                else:
                    raise ValueError(f'Invalid player data: {player}')
            document["players"] = players
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
        document.setdefault("game_state", None)
        document.setdefault("round_timer", None)
        document.setdefault("lives_per_player", None)
        document.setdefault("owner_id", None)
        document.setdefault("game_type", None)

        if "players" in document:
            players = []
            for player in document["players"]:
                if isinstance(player, dict):
                    players.append(Player(**player))
                else:
                    raise ValueError(f'Invalid player data: {player}')
            document["players"] = players
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
            document.setdefault("game_state", None)
            document.setdefault("round_timer", None)
            document.setdefault("lives_per_player", None)
            document.setdefault("owner_id", None)
            document.setdefault("game_type", None)

            if "players" in document:
                players = []
                for player in document["players"]:
                    if isinstance(player, str):
                        players.append(Player(player_id=player, player_name=player))
                    elif isinstance(player, dict):
                        players.append(Player(**player))
                document["players"] = players

            lobbies.append(LobbyRead(**document))
        return lobbies

    @staticmethod
    async def list_active_lobbies() -> List[LobbyRead]:
        """
        List all active lobbies
        @return: List[LobbyRead]
        """
        cursor = GameRepository.get_collection().find({"game_state": 1})
        lobbies = []
        for document in await cursor.to_list(length=None):
            document.setdefault("code", "None")
            document.setdefault("owner_name", "None")
            document.setdefault("game_state", None)
            document.setdefault("round_timer", None)
            document.setdefault("lives_per_player", None)
            document.setdefault("owner_id", None)
            document.setdefault("game_type", None)

            if "players" in document:
                players = []
                for player in document["players"]:
                    if isinstance(player, str):
                        players.append(Player(player_id=player, player_name=player))
                    elif isinstance(player, dict):
                        players.append(Player(**player))
                document["players"] = players

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

        for player in document["players"]:
            player["lives"] = document["lives_per_player"]

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
    async def add_player_to_lobby_by_id(lobby_id: str, player_id: str) -> LobbyRead:
        """
        Add a player to a lobby by its ID
        @param lobby_id: str
        @param player_id: str
        @return: LobbyRead
        """

        # Hole die Player-Informationen aus dem PlayerRepository
        player = await PlayerRepository.get(player_id)
        if not player:
            raise NotFoundException("Player not found")

        # Hole die Lobby-Informationen anhand der ID
        lobby_data = await GameRepository.get_by_id(lobby_id)

        # Setze die Leben des Spielers auf die Leben der Lobby und aktualisiere das lobby_id des Spielers
        player.lives = lobby_data.lives_per_player
        player.lobby_id = lobby_id

        # Aktualisiere das lobby_id und die Leben des Spielers in der Datenbank
        await PlayerRepository.update(player_id, PlayerUpdate(lobby_id=lobby_id, lives=player.lives))

        # Konvertiere die Player-Informationen in ein Dictionary
        player_dict = player.dict()

        # Füge den Player zur Lobby hinzu
        result = await GameRepository.get_collection().update_one(
            {"_id": str(lobby_id)},
            {"$addToSet": {"players": player_dict}}
        )
        if not result.modified_count:
            raise NotFoundException("Lobby not found or player already in lobby")
        return await GameRepository.get_by_id(lobby_id)

    @staticmethod
    async def add_player_to_lobby_by_code(code: str, player_id: str) -> LobbyRead:
        """
        Add a player to a lobby by its code
        @param code: str
        @param player_id: str
        @return: LobbyRead
        """

        # Hole die Player-Informationen aus dem PlayerRepository
        player = await PlayerRepository.get(player_id)
        if not player:
            raise NotFoundException("Player not found")

        # Hole die Lobby-Informationen anhand des Codes
        lobby_data = await GameRepository.get_by_code(code)
        lobby_id = lobby_data.lobby_id

        # Setze die Leben des Spielers auf die Leben der Lobby und aktualisiere das lobby_id des Spielers
        player.lives = lobby_data.lives_per_player
        player.lobby_id = lobby_id

        # Aktualisiere das lobby_id und die Leben des Spielers in der Datenbank
        await PlayerRepository.update(player_id, PlayerUpdate(lobby_id=lobby_id, lives=player.lives))

        # Konvertiere die Player-Informationen in ein Dictionary
        player_dict = player.dict()

        # Füge den Player zur Lobby hinzu
        result = await GameRepository.get_collection().update_one(
            {"code": code},
            {"$addToSet": {"players": player_dict}}
        )
        if not result.modified_count:
            raise NotFoundException("Lobby not found or player already in lobby")
        return await GameRepository.get_by_code(code)
