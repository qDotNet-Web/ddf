from bson import ObjectId
from fastapi import HTTPException
from app.models.game_model import LobbyCreate, LobbyRead, LobbyUpdate, PlayerCreate, PlayerRead, Question, Settings
from app.core.database import db
import random


async def get_game_collection():
    try:
        return db.db["game"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch game collection: {str(e)}")


async def get_questions_collection():
    try:
        print(db.db["questions"])
        return db.db["questions"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch questions collection: {str(e)}")


# CRUD operations for Game
def create_lobby_code():
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))


# CRUD operations for Lobby
async def create_lobby(lobby_data: LobbyCreate) -> LobbyCreate:
    collection = await get_game_collection()
    lobby_data.id = ObjectId(lobby_data.id)
    new_lobby = await collection.insert_one(lobby_data.dict(by_alias=True))
    created_lobby = await collection.find_one({"_id": new_lobby.inserted_id})
    if created_lobby:
        created_lobby["_id"] = str(created_lobby["_id"])
        return LobbyCreate(**created_lobby)
    else:
        raise HTTPException(status_code=404, detail="Lobby not created.")


async def get_lobby_by_id(lobby_id: str) -> LobbyRead:
    collection = await get_game_collection()
    lobby = await collection.find_one({"_id": ObjectId(lobby_id)})
    if lobby:
        lobby["_id"] = str(lobby["_id"])
        return LobbyRead(**lobby)
    else:
        raise HTTPException(status_code=404, detail="Lobby not found.")


async def get_lobby_by_owner(owner: PlayerRead) -> LobbyRead:
    collection = await get_game_collection()
    owner.id = ObjectId(owner.id)
    lobby = await collection.find_one({"owner": owner.dict(by_alias=True)})
    if lobby:
        lobby["_id"] = str(lobby["_id"])
        return LobbyRead(**lobby)
    else:
        raise HTTPException(status_code=404, detail="Lobby not found.")


async def get_lobby_by_code(code: str) -> LobbyRead:
    collection = await get_game_collection()
    lobby = await collection.find_one({"code": code})
    if lobby:
        lobby["_id"] = str(lobby["_id"])
        return LobbyRead(**lobby)
    else:
        raise HTTPException(status_code=404, detail="Lobby not found.")


async def update_lobby(lobby_id: str, lobby_data: LobbyUpdate) -> LobbyRead:
    collection = await get_game_collection()
    lobby_data.id = ObjectId(lobby_data.id)
    updated_lobby = await collection.update_one({"_id": ObjectId(lobby_id)}, {"$set": lobby_data.dict(by_alias=True)})
    if updated_lobby:
        return await get_lobby_by_id(lobby_id)
    else:
        raise HTTPException(status_code=404, detail="Lobby not updated.")


# CRUD operations for Player


# CRUD operations for Question
async def get_random_question() -> Question:
    collection = await get_questions_collection()
    try:
        sample = await collection.aggregate([{"$sample": {"size": 1}}]).to_list(1)
        if not sample:
            raise HTTPException(status_code=404, detail="No questions found.")
        random_question = sample[0]
        random_question["_id"] = str(random_question["_id"])
        return Question(**random_question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch question: {str(e)}")
