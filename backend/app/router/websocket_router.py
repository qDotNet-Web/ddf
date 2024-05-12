from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..crud.lobby_repo import lobby_manager

router = APIRouter()


@router.websocket("/{lobby_id}")
async def websocket_endpoint(websocket: WebSocket, lobby_id: str):
    await lobby_manager.connect(websocket, lobby_id)
    try:
        while True:
            data = await websocket.receive_text()
            await lobby_manager.broadcast(f'Nachricht erhalten von {lobby_id}: {data}')
    except WebSocketDisconnect:
        lobby_manager.disconnect(websocket)
        await lobby_manager.broadcast(f'Client {lobby_id} disconnected')
