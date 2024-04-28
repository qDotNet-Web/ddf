from ..models.game_model import LobbyModel
from ..schemas.game_schema import CreateLobby, Lobby
from typing import Dict
from uuid import uuid4


lobbies: Dict[str, Lobby] = {}


def create_lobby(lobby_data: CreateLobby) -> Lobby:
    lobby_id: str(uuid4())
    lobby = Lobby(
        id=lobby_id,
        timer=lobby_create.timer,
        lives_per_player=lobby_create.lives_per_player,
    )
    lobbies[lobby_id] = lobby
    return lobby
