from fastapi import WebSocket
from ..core.redis_client import redis_client
from typing import List, Dict
from ..models.game_model import LobbyCreate, LobbyUpdate, Player, LobbyRead
import json


class LobbyManager:
    def __init__(self, redis_instance):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.redis_instance = redis_instance

    async def handle_message(self, message: str, websocket: WebSocket):
        """
        Verarbeite eine Nachricht von einem WebSocket-Client.
        @param message:
        @param websocket:
        """
        message_data = json.loads(message)
        action = message_data.get('action')
        lobby_id = message_data.get('lobby_id')
        data = message_data.get('data', {})

        if action == 'update_lobby':
            await self.update_lobby(lobby_id, LobbyUpdate(**data))
        elif action == 'join_lobby_by_id':
            await self.join_lobby_by_id(lobby_id, data['player_id'], websocket)
        elif action == 'get_lobby_data':
            lobby_data = await self.get_lobby_data(lobby_id)
            await websocket.send_text(json.dumps(lobby_data))

    async def connect(self, websocket: WebSocket, lobby_id: str):
        """WebSocket-Verbindung akzeptieren und zur Lobby hinzufügen.
        @param websocket:
        @param lobby_id:
        """
        await websocket.accept()
        if lobby_id not in self.active_connections:
            self.active_connections[lobby_id] = []
        self.active_connections[lobby_id].append(websocket)

    def disconnect(self, websocket: WebSocket, lobby_id: str):
        """WebSocket-Verbindung aus einer Lobby entfernen.
        @param websocket:
        @param lobby_id:
        """
        if lobby_id in self.active_connections:
            self.active_connections[lobby_id].remove(websocket)
            if not self.active_connections[lobby_id]:
                del self.active_connections[lobby_id]
            print(f'Client {lobby_id} disconnected')

    async def broadcast(self, message: str, lobby_id: str):
        """Sende eine Nachricht an alle WebSocket-Verbindungen in einer Lobby.
        @param message:
        @param lobby_id:
        """
        for connection in self.active_connections.get(lobby_id, []):
            await connection.send_text(message)

    async def create_lobby(self, lobby_id: str, settings: LobbyCreate):
        """Erstelle eine neue Lobby in Redis mit den gegebenen Einstellungen.
        @param lobby_id:
        @param settings:
        """
        await self.redis_instance.set(f'lobby:{lobby_id}', settings.json())

    async def update_lobby(self, lobby_id: str, settings: LobbyUpdate):
        """Aktualisiere die Einstellungen einer bestehenden Lobby in Redis.
        @param lobby_id:
        @param settings:
        """
        lobby_data_json = await self.redis_instance.get(f'lobby:{lobby_id}')
        if not lobby_data_json:
            raise ValueError(f'Lobby with id {lobby_id} does not exist')
        lobby_data = json.loads(lobby_data_json)
        lobby_data.update(settings.dict(exclude_unset=True))
        await self.redis_instance.set(f'lobby:{lobby_id}', json.dumps(lobby_data))

    async def get_lobby_data(self, lobby_id: str) -> LobbyCreate:
        """Hole die Daten einer spezifischen Lobby aus Redis.
        @param lobby_id:
        @return: LobbyCreate
        """
        lobby_data_json = await self.redis_instance.get(f'lobby:{lobby_id}')
        if not lobby_data_json:
            raise ValueError(f'Lobby with id {lobby_id} does not exist')
        lobby_data = json.loads(lobby_data_json)
        return LobbyCreate(**lobby_data)

    async def get_active_lobbies(self) -> List[LobbyRead]:
        """Hole die Daten aller aktiven Lobbies aus Redis.
        @return: List[LobbyRead]
        """
        lobby_keys = await self.redis_instance.keys('lobby:*')
        lobby_data = await self.redis_instance.mget(lobby_keys)
        lobbies = []
        for data in lobby_data:
            if data:
                lobby = json.loads(data)
                lobby.setdefault("code", "None")
                lobby.setdefault("lobby_id", "None")  # Stelle sicher, dass 'lobby_id' vorhanden ist
                lobby.setdefault("owner_name", "None")
                lobby.setdefault("game_state", None)
                lobby.setdefault("round_timer", None)
                lobby.setdefault("lives_per_player", None)
                lobby.setdefault("owner_id", None)
                lobby.setdefault("game_type", None)
                if "players" in lobby:
                    players = []
                    for player in lobby["players"]:
                        if isinstance(player, str):
                            players.append(Player(player_id=player, player_name=player))
                        elif isinstance(player, dict):
                            players.append(Player(**player))
                    lobby["players"] = players
                lobbies.append(LobbyRead(**lobby))
            return lobbies

    async def join_lobby_by_id(self, lobby_id: str, player_id: str, websocket: WebSocket) -> None:
        """Füge einen Spieler zu einer Lobby hinzu.
        @param lobby_id:
        @param player_id:
        @param websocket:
        """
        lobby_data_json = await self.redis_instance.get(f'lobby:{lobby_id}')
        if not lobby_data_json:
            raise ValueError(f'Lobby with id {lobby_id} does not exist')
        lobby_data = json.loads(lobby_data_json)
        if any(p['player_id'] == player_id for p in lobby_data['players']):
            raise ValueError(f'Player with id {player_id} is already in the lobby')
        player_data = await self.redis_instance.get(f'player:{player_id}')
        if not player_data:
            raise ValueError(f'Player with id {player_id} does not exist')
        player = json.loads(player_data)
        lobby_data['players'].append(player)
        await self.redis_instance.set(f'lobby:{lobby_id}', json.dumps(lobby_data))
        await self.connect(websocket, lobby_id)
        await self.broadcast(json.dumps(lobby_data), lobby_id)

    async def create_player(self, player_name: str, player_id: str, lobby_id: str):
        """Erstelle einen neuen Spieler in einer Lobby in Redis.
        @param player_name:
        @param player_id:
        @param lobby_id:
        """
        player = Player(player_id=player_id, player_name=player_name)  # Verwenden Sie 'player_name' anstelle von 'name'
        lobby_data_json = await self.redis_instance.get(f'lobby:{lobby_id}')
        if not lobby_data_json:
            raise ValueError(f'Lobby with id {lobby_id} does not exist')
        lobby_data = json.loads(lobby_data_json)
        lobby_data['players'].append(player.dict())
        await self.redis_instance.set(f'lobby:{lobby_id}', json.dumps(lobby_data))

    async def get_player(self, player_id: str):
        """Hole die Daten eines Spielers aus einer Lobby in Redis.
        @param player_id:
        @return: object
        """
        player_data = await self.redis_instance.get(f'player:{player_id}')
        return json.loads(player_data) if player_data else None

    async def get_players(self, lobby_id: str) -> List[Player]:
        """Hole die Daten aller Spieler in einer Lobby aus Redis.
        @param lobby_id:
        @return: object
        """
        lobby_data_json = await self.redis_instance.get(f'lobby:{lobby_id}')
        if not lobby_data_json:
            raise ValueError(f'Lobby with id {lobby_id} does not exist')
        lobby_data = json.loads(lobby_data_json)
        return [Player(**player_data) for player_data in lobby_data['players']]

    async def remove_player(self, player_id: str):
        """Lösche einen Spieler aus einer Lobby in Redis.
        @param player_id:
        """
        await self.redis_instance.delete(f'player:{player_id}')

    async def save_lobby(self, lobby_id: str):
        from ..crud.game_repo import GameRepository
        """Speichere die Daten einer Lobby in der Datenbank."""
        lobby_data = await self.get_lobby_data(lobby_id)
        await GameRepository.save_lobby_from_redis(lobby_id, LobbyUpdate(**lobby_data))
        await self.redis_instance.delete(f'lobby:{lobby_id}')


lobby_manager = LobbyManager(redis_client)
