from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import List, Any


"""class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any):
        if not isinstance(v, ObjectId):
            raise TypeError("ObjectId required")
        return str(v)"""


class Player(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    name: str
    lives: int
    is_alive: bool = True


class Settings(BaseModel):
    round_timer: int = 180
    lives_per_player: int = 3


class Lobby(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    code: str
    owner: Player
    is_active: bool = False
    players: List[Player] = []
    settings: Settings


class Question(BaseModel):
    question: str
    answer: str
