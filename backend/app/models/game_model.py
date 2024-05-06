import pydantic
from pydantic import BaseModel, Field
from typing import Optional, List
from .fields import GameFields, PlayerFields, QuestionFields

__all__ = ("LobbyCreate", "LobbyRead", "LobbyUpdate", "PlayerCreate", "PlayerRead", "PlayerUpdate", "QuestionRead")


class LobbyUpdate(BaseModel):
    code: Optional[str] = GameFields.code
    # owner_id: Optional[str] = GameFields.owner_id
    owner_name: Optional[str] = GameFields.owner_name
    is_active: Optional[bool] = GameFields.is_active
    players: Optional[List[str]] = Field(default_factory=list)
    round_timer: Optional[int] = GameFields.round_timer
    lives_per_player: Optional[int] = GameFields.lives_per_player


class LobbyCreate(BaseModel):
    owner_name: str = GameFields.owner_name
    is_active: bool = GameFields.is_active
    players: List[str] = Field(default_factory=list)
    round_timer: int = GameFields.round_timer
    lives_per_player: int = GameFields.lives_per_player

    class Config:
        orm_mode = True


class LobbyRead(LobbyUpdate):
    code: str = GameFields.code

    @pydantic.root_validator(pre=True)
    def _set_lobby_id(cls, data):
        document_id = data.get("_id")
        if document_id:
            data["lobby_id"] = document_id
        return data

    class Config(LobbyCreate.Config):
        extra = pydantic.Extra.ignore


class PlayerUpdate(BaseModel):
    name: Optional[str] = PlayerFields.name
    lives: Optional[int] = PlayerFields.lives
    is_alive: Optional[bool] = PlayerFields.is_alive


class PlayerCreate(PlayerUpdate):
    name: str = PlayerFields.name
    lives: int = PlayerFields.lives
    is_alive: bool = PlayerFields.is_alive


    class Config:
        orm_mode = True


class PlayerRead(PlayerCreate):
    @pydantic.root_validator(pre=True)
    def _set_player_id(cls, data):
        document_id = data.get("_id")
        if document_id:
            data["player_id"] = document_id
        return data

    class Config(PlayerCreate.Config):
        extra = pydantic.Extra.ignore


class QuestionRead(BaseModel):
    question: Optional[str] = QuestionFields.question
    answer: Optional[str] = QuestionFields.answer

    class Config:
        extra = pydantic.Extra.ignore
        orm_mode = True
