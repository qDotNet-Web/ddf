from fastapi import APIRouter
from ...crud.repositories import PlayerRepository
from ...models.game_model import PlayerRead, PlayerCreate, PlayerUpdate
from typing import List


router = APIRouter()


@router.get("/",
            response_model=List[PlayerRead],
            summary="List all players",
            description="List all players in the database",
            tags=["player"])
async def list_players_route():
    return await PlayerRepository.list()

