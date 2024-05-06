from fastapi import APIRouter, HTTPException, status
from ...crud.repositories import GameRepository, QuestionRepository
from ...models.game_model import LobbyRead, LobbyUpdate, PlayerCreate, PlayerUpdate, QuestionRead, LobbyCreate

router = APIRouter()


@router.get("/lobby",
            response_model=LobbyRead,
            description="List all available lobbies",
            tags=["lobby"])
async def list_lobbies():
    return await GameRepository.list()


@router.post("/lobby/create",
             response_model=LobbyCreate,
             description="Create a new lobby",
             tags=["lobby"])
async def create_lobby(lobby: LobbyCreate):
    return await GameRepository.create(lobby)


@router.get("/lobby/get/{lobby_id}", response_model=LobbyRead, description="Get a lobby by id", tags=["lobby"])
async def get_lobby(lobby_id: str):
    return await GameRepository.get(lobby_id)


@router.get("/question/get_random_question",
            response_model=QuestionRead,
            description="Get a random question",
            tags=["question"])
async def get_random_question_route():
    return await QuestionRepository.get_random()


async def update_lobby(lobby_id: str, lobby: LobbyUpdate):
    raise NotImplementedError("update_lobby not implemented yet")
