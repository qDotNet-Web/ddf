from fastapi import APIRouter, HTTPException
from ..crud.player_repo import PlayerRepository
from ..models.game_model import PlayerRead, PlayerCreate, PlayerUpdate
from typing import List


router = APIRouter()


@router.get("/get_all_players",
            response_model=List[PlayerRead],
            summary="List all players",
            description="List all players in the database",
            tags=["player"])
async def list_players_route():
    try:
        return await PlayerRepository.list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_player/",
             response_model=PlayerRead,
             description="Create a new player",
             tags=["player"])
async def create_player(player_create: PlayerCreate) -> PlayerRead:
    try:
        return await PlayerRepository.create_player(player_create)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
