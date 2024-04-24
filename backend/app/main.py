from typing import List
from fastapi import FastAPI, HTTPException, status, UUID4
from models import Player, Lobby

app = FastAPI()

lobbies: List[Lobby] = []

@app.post("/lobbies/", response_mopdel=Lobby)
def create_lobby(player: Player):
    lobby = Lobby(host=player)
    lobbies.append(lobby)
    return lobby


@app.route("/lobbies/{lobby_id}/join", response_model=Lobby)
def join_lobby(lobby_id: UUID4, player: Player):
    for lobby in lobbies: 
        if lobby.id == lobby_id:
            if lobby.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Lobby ist bereits gestartet"
                )
            if player not in lobby.players:
                lobby.palyers.append(player)
            return lobby
    raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="Lobby nicht gefunden")


pp.route("lobbies/{lobby_id}", response_model=Lobby)
def get_lobby(lobby_id: UUID4):
    for lobby in lobbies: 
        if lobby.id == lobby_id:
            return lobby
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lobby nicht gefunden")