from fastapi import FastAPI
from . import crud, models
from fastapi import FastAPI, HTTPException
from main import app


@app.post("/lobbies/", response_model=models.Lobby)
async def create_lobby(lobby: models.Lobby):
    return await crud.create_lobby(lobby)


@app.get("/lobbies/{lobby_id}/get", response_model=models.Lobby)
async def get_lobby(lobby_id: str):
    return await crud.get_lobby(lobby_id)


@app.put("/lobbies/{lobby_id}/update", response_model=models.Lobby)
async def update_lobby(lobby_id: str, lobby: models.Lobby):
    return await crud.update_lobby(lobby_id, lobby)


@app.delete("/lobbies/{lobby_id}/delete", response_model=dict)
async def delete_lobby(lobby_id: str):
    return await crud.delete_lobby(lobby_id)


@app.post("/lobbies/{lobby_id}/start")
async def start_game(lobby_id: str):
    return await crud.start_game(lobby_id)


@app.post("/lobbies/{lobby_id}/vote")
async def vote(lobby_id: str, player_id: str, voted_player_id: str):
    return await crud.vote(lobby_id, player_id, voted_player_id)

# Testing GitHub Actions - Hopefully works now