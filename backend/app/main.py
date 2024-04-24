from fastapi import FastAPI
from . import crud, models
from .database import connect_to_mongo, clode_mongo_connection

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    await clode_mongo_connection()


@app.post("/lobbies/", response_model=models.Lobby)
async def create_lobby(lobby: models.Lobby):
    return await crud.create_lobby(lobby)


@app.get("/lobbies/{lobby_id}", response_model=models.Lobby)
async def read_lobby(lobby_id: str):
    return await crud.get_lobby(lobby_id)


@app.put("/lobbies/{lobby_id}", response_model=models.Lobby)
async def upadte_lobby(lobby_id: str, lobby: models.Lobby):
    return await crud.update_lobby(lobby_id, lobby)


@app.delete("/lobbies/{lobby_id}", response_model=dict)
async def delete_lobby(lobby_id: str):
    return await crud.delete_lobby(lobby_id)


@app.post("/lobbies/{lobby_id}/start")
async def start_game(lobby_id: str):
    return await crud.start_game(lobby_id)


@app.post("/lobbies/{lobby_id}/vote")
async def vote(lobby_id: str, player_id: str, voted_player_id: str):
    return await crud.vote(lobby_id, player_id, voted_player_id)