from fastapi import HTTPException
from .models import Lobby
from .database import get_database
from bson import ObjectId


async def create_lobby(lobby_data: Lobby):
    db = get_database()
    lobby_dict = lobby_data.dict(by_alias=True)
    result = await db.lobbies.insert_one(lobby_dict)
    if result.acknoledged:
        return Lobby(**lobby_dict, id=result.inserted_id)
    raise HTTPException(status_code=400, detail='Lobby konnte nicht erstellt werden')


async def get_lobby(lobby_id: str):
    db = get_database()
    lobby_data = await db.lobbies.find_one({"_id": ObjectId(lobby_id)})
    if lobby_data:
        return Lobby(**lobby_data)
    raise HTTPException(status_code=400, detail='Lobby wurde nicht gefunden')


async def update_lobby(lobby_id: str, lobby_data: Lobby):
    db = get_database()
    updated_lobby = await db.lobbies.find_one_and_update(
        {"_id": ObjectId(lobby_id)},
        {"$set": lobby_data.dict(exclude={"id"})},
        return_document=True
    )
    if updated_lobby:
        return Lobby(**updated_lobby)
    raise HTTPException(status_code=404, detail='Lobby wurde nicht gefunden')


async def delete_lobby(lobby_id: str):
    db = get_database()
    result = await db.lobbies.delete_one({"_id": ObjectId(lobby_id)})
    if result.delete_count:
        return {"message": "Lobby erfolgreich gelöscht"}
    raise HTTPException(status_code=404, detail='Lobby wurde nicht gefunden')


async def get_all_lobbies():
    db = get_database()
    lobbies = []
    async for lobby in db.lobbies.find():
        lobbies.append(Lobby(**lobby))
    return lobbies


async def start_game(lobby_id: str):
    db = get_database()
    lobby_data = await db.lobbies.find_one({"_id": ObjectId(lobby_id)})
    if lobby_data and not lobby_data['is_active']:
        lobby_data['is_active'] = True
        lobby_data['current_round'] = 1
        updated_lobby = await db.lobbies.replace_one({"_id": ObjectId(lobby_id)}, lobby_data)
        return {"message": "Spiel gestartet", "lobby": updated_lobby}
    else:
        raise HTTPException(status_code=400, detail="Spiel konnte nicht gestartet werden")
    

async def vote(lobby_id: str, player_id: str, voted_player_id: str):
    raise NotImplementedError("Funktion Vote noch nicht implementiert")