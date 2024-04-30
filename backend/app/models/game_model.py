from pydantic import BaseModel, Field
from typing import List, Any


class PlayerCreate(BaseModel):
    name: str


class PlayerRead(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    name: str
    lives: int
    is_alive: bool


class PlayerUpdate(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    name: str
    lives: int
    is_alive: bool


class Settings(BaseModel):
    round_timer: int = 180
    lives_per_player: int = 3


class LobbyRead(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    code: str
    owner: PlayerRead
    is_active: bool = False
    players: List[PlayerRead] = []
    settings: Settings


class LobbyCreate(BaseModel):
    owner: PlayerCreate
    settings: Settings


class LobbyUpdate(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    code: str
    owner: PlayerRead
    is_active: bool = False
    players: List[PlayerRead] = []
    settings: Settings


class Question(BaseModel):
    question: str
    answer: str
