from pydantic import BaseModel, Field
from typing import List


class PlayerCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class PlayerRead(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    name: str
    lives: int
    is_alive: bool

    class Config:
        orm_mode = True


class PlayerUpdate(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    name: str
    lives: int
    is_alive: bool

    class Config:
        orm_mode = True


class PlayerJoin(BaseModel):
    name: str
    lives: int
    is_alive: bool

    class Config:
        orm_mode = True


class Settings(BaseModel):
    round_timer: int = 180
    lives_per_player: int = 3
    max_players: int = 10

    class Config:
        orm_mode = True


class LobbyRead(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    code: str
    owner: PlayerRead
    is_active: bool = False
    players: List[PlayerRead] = []
    settings: Settings

    class Config:
        orm_mode = True


class LobbyCreate(BaseModel):
    owner: PlayerCreate
    settings: Settings

    class Config:
        orm_mode = True


class LobbyUpdate(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    code: str
    owner: PlayerRead
    is_active: bool = False
    players: List[PlayerRead] = []
    settings: Settings

    class Config:
        orm_mode = True


class Question(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    question: str
    correct_answer: str

    class Config:
        orm_mode = True
