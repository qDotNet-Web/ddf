from bson import ObjectId
from fastapi import HTTPException
from ..models.game_model import Lobby, Player, Question, Settings
from ..core.database import db


async def get_game_collection():
    return db.db["game"]


# CRUD operations for Lobby
async def create_lobby(lobby_data: Lobby) -> Lobby:
    # Zugriff auf die Collection direkt in der Funktion
    collection = await get_game_collection()
    lobby_data.id = ObjectId(lobby_data.id)
    new_lobby = await collection.insert_one(lobby_data.dict(by_alias=True))
    created_lobby = await collection.find_one({"_id": new_lobby.inserted_id})
    if created_lobby:
        created_lobby["_id"] = str(created_lobby["_id"])
        return Lobby(**created_lobby)
    else:
        # Geeignete Fehlerbehandlung hinzufügen
        raise HTTPException(status_code=404, detail="Lobby not created.")


async def get_lobby_by_id(lobby_id: str) -> Lobby:
    collection = await get_game_collection()
    lobby = await collection.find_one({"_id": ObjectId(lobby_id)})
    if lobby:
        lobby["_id"] = str(lobby["_id"])
        return Lobby(**lobby)
    else:
        # Geeignete Fehlerbehandlung hinzufügen
        raise HTTPException(status_code=404, detail="Lobby not found.")


async def get_lobby_by_owner(owner: Player) -> Lobby:
    collection = await get_game_collection()
    owner.id = ObjectId(owner.id)
    lobby = await collection.find_one({"owner": owner.dict(by_alias=True)})
    if lobby:
        lobby["_id"] = str(lobby["_id"])
        return Lobby(**lobby)
    else:
        # Geeignete Fehlerbehandlung hinzufügen
        raise HTTPException(status_code=404, detail="Lobby not found.")


# CRUD operations for Player


# CRUD operations for Question
