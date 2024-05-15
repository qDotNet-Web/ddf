import pydantic
from pydantic import BaseModel, Field
from typing import Optional, List
from .fields import GameFields, PlayerFields, QuestionFields

__all__ = ("LobbyCreate", "LobbyRead", "LobbyUpdate", "PlayerCreate", "PlayerRead", "PlayerUpdate", "QuestionRead")


class LobbyUpdate(BaseModel):
    code: Optional[str] = GameFields.code
    owner_id: Optional[str] = GameFields.owner_id
    owner_name: Optional[str] = GameFields.owner_name
    is_active: Optional[bool] = GameFields.is_active
    players: Optional[List[str]] = Field(default_factory=list)
    round_timer: Optional[int] = GameFields.round_timer
    lives_per_player: Optional[int] = GameFields.lives_per_player
    text_based: Optional[bool] = GameFields.text_based


class LobbyCreate(BaseModel):
    owner_id: Optional[str] = GameFields.owner_id
    owner_name: str = GameFields.owner_name
    is_active: bool = GameFields.is_active
    players: List[str] = Field(default_factory=list)
    round_timer: int = GameFields.round_timer
    lives_per_player: int = GameFields.lives_per_player
    text_based: Optional[bool] = GameFields.text_based
    used_questions: Optional[List[str]] = Field(default_factory=list)

    class Config:
        orm_mode = True


class LobbyQuestions(BaseModel):
    lobby_id: str = GameFields.lobby_id
    question_id: List[str] = QuestionFields.question_id
    used: bool = QuestionFields.used


class LobbyRead(LobbyUpdate):
    lobby_id: str = Field(description="The id of the lobby")
    code: str = GameFields.code

    @pydantic.model_validator(mode="before")
    def _set_lobby_id(cls, data):
        if isinstance(data, dict):
            document_id = data.get('_id')
            if document_id:
                data["lobby_id"] = str(document_id)
        return data

    class Config(LobbyCreate.Config):
        orm_mode = True
        extra = pydantic.Extra.ignore


class PlayerUpdate(BaseModel):
    name: Optional[str] = PlayerFields.name
    lives: Optional[int] = PlayerFields.lives
    is_alive: Optional[bool] = PlayerFields.is_alive
    avatar_id: Optional[int] = PlayerFields.avatar_id


class PlayerCreate(BaseModel):
    name: str = PlayerFields.name
    # lobby_id: str = GameFields.lobby_id
    avatar_id: int = PlayerFields.avatar_id

    class Config:
        orm_mode = True


class PlayerRead(PlayerCreate):
    name: str = PlayerFields.name
    player_id: str = PlayerFields.player_id
    avatar_id: int = PlayerFields.avatar_id

    @pydantic.model_validator(mode="before")
    def _set_player_id(cls, data):
        if isinstance(data, dict):
            document_id = data.get("_id")
            if document_id:
                data["player_id"] = document_id
        return data

    class Config(PlayerCreate.Config):
        extra = pydantic.Extra.ignore


class QuestionRead(BaseModel):
    question: Optional[str] = QuestionFields.question
    correct_answer: Optional[str] = QuestionFields.answer

    class Config:
        extra = pydantic.Extra.ignore
        orm_mode = True
