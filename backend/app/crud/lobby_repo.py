from fastapi import WebSocket

from ..core.redis_client import redis_client
from typing import List, Dict
from ..models.game_model import LobbyCreate, LobbyUpdate
import json


class LobbyManager:
    def __init__(self, redis_instance):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.redis_instance = redis_instance

    async def handle_message(self, message: str, websocket: WebSocket):
        message_data = json.loads(message)
        action = message_data.get('action')
        lobby_id = message_data.get('lobby_id')
        data = message_data.get('data', {})

        if action == 'create_lobby':
            await self.create_lobby(lobby_id, LobbyCreate(**data))
        elif action == 'update_lobby':
            await self.update_lobby(lobby_id, LobbyUpdate(**data))
        elif action == 'get_lobby_data':
            lobby_data = await self.get_lobby_data(lobby_id)
            await websocket.send_text(json.dumps(lobby_data))

    async def connect(self, websocket: WebSocket, lobby_id: str):
        """WebSocket-Verbindung akzeptieren und zur Lobby hinzufügen."""
        await websocket.accept()
        if lobby_id not in self.active_connections:
            self.active_connections[lobby_id] = []
        self.active_connections[lobby_id].append(websocket)

    def disconnect(self, websocket: WebSocket, lobby_id: str):
        """WebSocket-Verbindung aus einer Lobby entfernen."""
        if lobby_id in self.active_connections:
            self.active_connections[lobby_id].remove(websocket)
            if not self.active_connections[lobby_id]:
                del self.active_connections[lobby_id]
            print(f'Client {lobby_id} disconnected')

    async def broadcast(self, message: str, lobby_id: str):
        """Sende eine Nachricht an alle WebSocket-Verbindungen in einer Lobby."""
        for connection in self.active_connections.get(lobby_id, []):
            await connection.send_text(message)

    async def create_lobby(self, lobby_id: str, settings: LobbyCreate):
        """Erstelle eine neue Lobby in Redis mit den gegebenen Einstellungen."""
        await self.redis_instance.client.set(f'lobby:{lobby_id}', settings.json())

    async def update_lobby(self, lobby_id: str, settings: LobbyUpdate):
        """Aktualisiere die Einstellungen einer bestehenden Lobby in Redis."""
        lobby_data_json = await self.redis_instance.client.get(f'lobby:{lobby_id}')
        if not lobby_data_json:
            raise ValueError(f'Lobby with id {lobby_id} does not exist')
        lobby_data = json.loads(lobby_data_json)
        lobby_data.update(settings.dict(exclude_unset=True))
        await self.redis_instance.client.set(f'lobby:{lobby_id}', json.dumps(lobby_data))

    async def get_lobby_data(self, lobby_id: str):
        """Hole die Daten einer spezifischen Lobby aus Redis."""
        lobby_data_json = await self.redis_instance.client.get(f'lobby:{lobby_id}')
        if not lobby_data_json:
            raise ValueError(f'Lobby with id {lobby_id} does not exist')
        return json.loads(lobby_data_json)

    async def get_active_lobbies(self):
        """Hole die Daten aller aktiven Lobbies aus Redis."""
        lobby_keys = await self.redis_instance.client.keys('lobby:*')
        lobby_data = await self.redis_instance.client.mget(*lobby_keys)
        return [json.loads(data) for data in lobby_data]

    async def create_player(self, player_name: str, player_id: str, lobby_id: str):
        """Erstelle einen neuen Spieler in einer Lobby in Redis."""
        await self.redis_instance.client.set(f'lobby:{lobby_id}:player:{player_id}', player_name)

    async def get_player(self, player_id: str):
        """Hole die Daten eines Spielers aus einer Lobby in Redis."""
        player_data = await self.redis_instance.client.get(f'player:{player_id}')
        return json.loads(player_data)

    async def get_players(self, lobby_id: str):
        """Hole die Daten aller Spieler in einer Lobby aus Redis."""
        player_keys = await self.redis_instance.client.keys(f'lobby:{lobby_id}:player:*')
        player_data = await self.redis_instance.client.mget(*player_keys)
        return [json.loads(data) for data in player_data]

    async def delete_player(self, player_id: str):
        """Lösche einen Spieler aus einer Lobby in Redis."""
        await self.redis_instance.client.delete(f'player:{player_id}')

    async def save_lobby(self, lobby_id: str):
        from .game_repo import GameRepository
        """Speichere die Daten einer Lobby in der Datenbank."""
        lobby_data = await self.get_lobby_data(lobby_id)
        await GameRepository.save_lobby_from_redis(lobby_data)


lobby_manager = LobbyManager(redis_client)
