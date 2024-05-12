from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..crud.lobby_repo import lobby_manager

router = APIRouter()


@router.websocket("/{lobby_id}")
async def websocket_endpoint(websocket: WebSocket, lobby_id: str):
    await lobby_manager.connect(websocket, lobby_id)
    try:
        while True:
            data = await websocket.receive_text()
            await lobby_manager.handle_message(data, websocket)
    except WebSocketDisconnect:
        lobby_manager.disconnect(websocket)
        await lobby_manager.broadcast(f'Client {lobby_id} disconnected')


"""
example:

<script>
export default {
  data() {
    return {
      ws: null,
    };
  },
  methods: {
    connectToWebSocket() {
      this.ws = new WebSocket('ws://localhost:8000/ws/lobby123');

      this.ws.onopen = () => {
        this.sendAction('create_lobby', {
          lobby_name: "Example Lobby",
          settings: {
            max_players: 10
          }
        });
      };
    },
    sendAction(action, data) {
      const message = JSON.stringify({ action, data });
      this.ws.send(message);
    }
  },
  mounted() {
    this.connectToWebSocket();
  }
};
</script>

"""