from fastapi import APIRouter, HTTPException
from ..crud.game_repo import GameRepository
from ..models.game_model import LobbyRead, LobbyCreate, LobbyUpdate
from ..crud.lobby_repo import lobby_manager
from ..core.utils import sio
from typing import List


router = APIRouter()


@router.get("/get_all_lobbies",
            response_model=List[LobbyRead],
            description="List all available lobbies",
            tags=["lobby"])
async def list_lobbies():
    try:
        return await GameRepository.list()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/get_all_active_lobbies",
            response_model=List[LobbyRead],
            description="List all active lobbies",
            tags=["lobby"])
async def list_active_lobbies():
    try:
        return await GameRepository.list_active_lobbies()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/create_lobby",
             response_model=LobbyRead,
             description="Create a new lobby",
             tags=["lobby"])
async def create_lobby(lobby_id: str, lobby_data: LobbyCreate):
    try:
        return await GameRepository.create(lobby_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_by_id/{lobby_id}",
            response_model=LobbyRead,
            description="Get a lobby by id",
            tags=["lobby"])
async def get_lobby_by_id(lobby_id: str):
    try:
        return await GameRepository.get_by_id(lobby_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/get_by_code/{code}",
            response_model=LobbyRead,
            description="Get a lobby by code",
            tags=["lobby"])
async def get_lobby_by_code(code: str):
    try:
        return await GameRepository.get_by_code(code)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/join_id/{lobby_id}",
             response_model=LobbyRead,
             description="Add a player to a lobby by id",
             tags=["lobby"])
async def add_player_to_lobby_by_id(lobby_id: str, player_id: str, player_name: str):
    try:
        return await GameRepository.add_player_to_lobby_by_id(lobby_id, player_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/join_code/{code}",
             response_model=LobbyUpdate,
             description="Add a player to a lobby by code",
             tags=["lobby"])
async def add_player_to_lobby_by_code(code: str, player_id: str, player_name: str):
    try:
        return await GameRepository.add_player_to_lobby_by_code(code, player_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    session = await sio.get_session(sid)
    lobby_id = session.get("lobby_id")
    if lobby_id:
        lobby_manager.disconnect(sid, lobby_id)


@sio.event
async def join(sid, data):
    lobby_id = data["lobby_id"]
    player_id = data["player_id"]
    await lobby_manager.connect(sid, lobby_id)
    await sio.emit('player_joined', {"player_id": player_id}, room=sid)


@sio.event
async def submit_answer(sid, data):
    # Implementiere die Logik für das Einsenden von Antworten
    pass


@sio.event
async def vote(sid, data):
    # Implementiere die Logik für das Voting
    pass
