from typing import List, Dict
from ..core.utils import sio
from ..crud.game_repo import GameRepository
import json


class LobbyManager:
    def __init__(self):
        self.active_connections: Dict[str, List[str]] = {}

    async def handle_message(self, message: str, sid: str):
        """
        Handle incoming messages from Socket.IO
        @param message:
        @param sid:
        """
        message_data = json.loads(message)
        action = message_data.get('action')
        lobby_id = message_data.get('lobby_id')
        data = message_data.get('data', {})

        if action == 'get_lobby_data':
            lobby_data = await GameRepository.get_by_id(lobby_id)
            await sio.emit('lobby_data', lobby_data, room=sid)

    async def connect(self, sid: str, lobby_id: str):
        """Socket.IO-Verbindung akzeptieren und zur Lobby hinzufügen.
        @param sid:
        @param lobby_id:
        """
        await sio.save_session(sid, {"lobby_id": lobby_id})
        if lobby_id not in self.active_connections:
            self.active_connections[lobby_id] = []
        self.active_connections[lobby_id].append(sid)

    def disconnect(self, sid: str, lobby_id: str):
        """Socket.IO-Verbindung aus einer Lobby entfernen.
        @param sid:
        @param lobby_id:
        """
        if lobby_id in self.active_connections:
            self.active_connections[lobby_id].remove(sid)
            if not self.active_connections[lobby_id]:
                del self.active_connections[lobby_id]
            print(f'Client {sid} disconnected from lobby {lobby_id}')

    async def broadcast(self, message: str, lobby_id: str):
        """Sende eine Nachricht an alle Socket.IO-Verbindungen in einer Lobby.
        @param message:
        @param lobby_id:
        """
        await sio.emit('message', message, room=lobby_id)


lobby_manager = LobbyManager()
