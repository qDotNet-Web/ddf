from fastapi import APIRouter, HTTPException, status
from ...schemas.game_schema import Lobby, CreateLobby, Player, Question, Vote
from ...crud.game_crud import create_lobby, get_lobby, add_player, start_game, end_game, submit_answer, process_vote


router = APIRouter()

lobbies = {}


@router.post("/create", response_model=Lobby)
async def create_lobby_endpoint(lobby_data: CreateLobby) -> Lobby:
    return create_lobby(lobby_data)


@router.get("/{code}", response_model=Lobby)
async def get_lobby_endpoint(code: str) -> Lobby:
    lobby = get_lobby(code)
    if not lobby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lobby not found")
    return lobby


@router.post("/{code}/join", response_model=Lobby)
async def join_lobby_endpoint(code: str, player_name: str):
    try:
        return add_player(code, player_name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{code}/start")
async def start_game_endpoint(code: str):
    if not start_game(code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game could not be started")
    return {"message": "Game started"}


@router.post("/{code}/answer", response_model=Lobby)
async def submit_answer_endpoint(code: str, player_name: str, answer: str):
    try:
        return submit_answer(code, player_name, answer)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{code}/vote", response_model=Lobby)
async def vote_endpoint(code: str, vote: Vote):
    try:
        return process_vote(code, vote.voter, vote.votee)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
