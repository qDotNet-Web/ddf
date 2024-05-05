from fastapi import APIRouter, HTTPException, status
from ...crud.repositories import GameRepository, QuestionRepository
from ...models.game_model import LobbyRead, LobbyUpdate, PlayerCreate, PlayerUpdate, QuestionRead


router = APIRouter()


@router.get("/lobby",
            response_model=LobbyRead,
            description="List all available lobbies",
            tags=["lobby"])
async def list_lobbies():
    return GameRepository.list()


@router.get("/question/get_random_question",
            response_model=QuestionRead,
            description="Get a random question",
            tags=["question"])
async def get_random_question_route():
    return QuestionRepository.get_random()


async def update_lobby(lobby_id: str, lobby: LobbyUpdate):
    raise NotImplementedError("update_lobby not implemented yet")
