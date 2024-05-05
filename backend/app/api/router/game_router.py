from fastapi import APIRouter, HTTPException, status
from app.models.game_model import (LobbyCreate, LobbyRead, LobbyUpdate, PlayerCreate, PlayerRead, PlayerUpdate, PlayerJoin
, Question, Settings)
from app.crud.game_crud import create_lobby, get_lobby_by_id, get_lobby_by_owner, get_random_question


router = APIRouter()


@router.post("/lobby/create")
async def create_lobby_route(lobby_data: LobbyCreate):
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


@router.get("/lobby/owner/{owner_id}")
async def get_lobby_by_owner_route(owner_id: str):
    try:
        owner = PlayerRead(id=owner_id)
        lobby = await get_lobby_by_owner(owner)
        if lobby:
            return lobby
        else:
            raise HTTPException(status_code=404, detail="Lobby not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lobby/{lobby_id}/join")
async def join_lobby_route(lobby_data: LobbyRead, lobby_id: str, player_data: PlayerJoin):
    try:
        lobby = await get_lobby_by_id(lobby_id)
        if not lobby:
            raise HTTPException(status_code=404, detail="Lobby not found")
        new_player = PlayerCreate(name=player_data.name, lives=player_data.lives, is_alive=True)

        if len(lobby.players) >= lobby_data.settings.max_players:
            raise HTTPException(status_code=400, detail="Lobby is full")

        lobby.players.append(new_player)

        updated_lobby = await update_lobby(lobby_id, lobby)
        return updated_lobby
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException as e:
        raise e


@router.get("/question/get_random_question")
async def get_random_question():
    try:
        question = await get_random_question()
        return question
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_lobby(lobby_id: str, lobby: LobbyUpdate):
    raise NotImplementedError("update_lobby not implemented yet")