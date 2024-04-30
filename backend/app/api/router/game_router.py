from fastapi import APIRouter, HTTPException, status
from ...models.game_model import Lobby, Player, Question, Settings
from ...crud.game_crud import create_lobby, get_lobby_by_id, get_lobby_by_owner


router = APIRouter()


@router.post("/lobby/create")
async def create_lobby_route(lobby_data: Lobby):
    try:
        created_lobby = await create_lobby(lobby_data)
        return created_lobby
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lobby/{lobby_id}")
async def get_lobby_by_id_route(lobby_id: str):
    try:
        lobby = await get_lobby_by_id(lobby_id)
        if lobby:
            return lobby
        else:
            raise HTTPException(status_code=404, detail="Lobby not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

