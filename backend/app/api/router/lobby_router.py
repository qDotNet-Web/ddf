from fastapi import APIRouter
from ...crud.repositories import GameRepository
from ...models.game_model import LobbyRead, LobbyCreate, LobbyUpdate
from typing import List


router = APIRouter()


@router.get("/get_all_lobbies",
            response_model=List[LobbyRead],
            description="List all available lobbies",
            tags=["lobby"])
async def list_lobbies():
    return await GameRepository.list()


@router.post("/create_lobby",
             response_model=LobbyCreate,
             description="Create a new lobby",
             tags=["lobby"])
async def create_lobby(lobby: LobbyCreate):
    return await GameRepository.create(lobby)


@router.get("/get/{lobby_id}", response_model=LobbyRead, description="Get a lobby by id", tags=["lobby"])
async def get_lobby(lobby_id: str):
    return await GameRepository.get(lobby_id)