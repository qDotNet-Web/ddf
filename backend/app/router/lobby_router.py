from fastapi import APIRouter, HTTPException
from ..crud.game_repo import GameRepository
from ..models.game_model import LobbyRead, LobbyCreate, LobbyUpdate, PlayerRead, PlayerCreate
from ..crud.lobby_repo import lobby_manager
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
        return await lobby_manager.get_active_lobbies()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/create_lobby",
             response_model=LobbyRead,
             description="Create a new lobby",
             tags=["lobby"])
async def create_lobby(lobby: LobbyCreate):
    try:
        return await GameRepository.create(lobby)
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
async def add_player_to_lobby_by_id(lobby_id: str, player_name: str):
    try:
        return await GameRepository.add_player_to_lobby_by_id(lobby_id, player_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/join_code/{code}",
             response_model=LobbyRead,
             description="Add a player to a lobby by code",
             tags=["lobby"])
async def add_player_to_lobby_by_code(code: str, player_name: str):
    try:
        return await GameRepository.add_player_to_lobby_by_code(code, player_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
