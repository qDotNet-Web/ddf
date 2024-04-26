from fastapi import APIRouter


router = APIRouter()

@router.post("/game/")
def create_game():
    return {"message": "Spiel erstellt"}