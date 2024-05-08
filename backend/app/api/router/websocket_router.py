from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ...core.websockets import connection_manager

router = APIRouter()


@router.websocket("/{lobby_code}")
async def websocket_endpoint(websocket: WebSocket, lobby_code: str):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.broadcast(f'Nachricht erhalten von {lobby_code}: {data}')
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await connection_manager.broadcast(f'Client {lobby_code} disconnected')
