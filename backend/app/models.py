from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)


class Player(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str
    avatar: Optional[str] = None


class Lobby(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    host: Player
    players: List[Player] = []
    is_active: bool = False
    max_players: int
    lives: int
    rounds: int
    text_based: bool = False
