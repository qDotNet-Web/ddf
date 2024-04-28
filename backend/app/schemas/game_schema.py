from pydantic import BaseModel, Field, UUID4
from typing import List
from uuid import uuid4


class CreateLobby(BaseModel):
    timer: int
    lives_per_player: int


class Lobby(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    code: str
    timer: int
    lives_per_player: int
    players: List[str] = []


class Question(BaseModel):
    text: str
    answer: str


class Player(BaseModel):
    name: str
