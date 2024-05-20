import pydantic
from pydantic import BaseModel, Field
from typing import Optional, List
from .fields import GameFields, PlayerFields, QuestionFields

__all__ = ("LobbyCreate", "LobbyRead", "LobbyUpdate", "PlayerCreate", "PlayerRead", "PlayerUpdate", "QuestionRead", "Player")


class Player(BaseModel):
    player_id: str = PlayerFields.player_id
    player_name: str = PlayerFields.player_name
    lives: int = PlayerFields.lives


class LobbyUpdate(BaseModel):
    code: Optional[str] = GameFields.code
    owner_id: Optional[str] = GameFields.owner_id
    owner_name: Optional[str] = GameFields.owner_name
    game_state: Optional[int] = GameFields.game_state
    players: Optional[List[Player]] = Field(default_factory=list)
    round_timer: Optional[int] = GameFields.round_timer
    lives_per_player: Optional[int] = GameFields.lives_per_player
    game_type: Optional[int] = GameFields.game_type
    used_questions: Optional[List[int]] = Field(default_factory=list)


class LobbyCreate(BaseModel):
    # code: Optional[str] = GameFields.code
    owner_id: Optional[str] = GameFields.owner_id
    owner_name: str = GameFields.owner_name
    game_state: int = GameFields.game_state
    players: List[Player] = Field(default_factory=list)
    round_timer: int = GameFields.round_timer
    lives_per_player: int = GameFields.lives_per_player
    game_type: int = GameFields.game_type
    used_questions: Optional[List[int]] = Field(default_factory=list)

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
    player_name: Optional[str] = None
    lobby_id: Optional[str] = None
    lives: Optional[int] = None
    player_state: Optional[int] = None
    avatar_id: Optional[int] = None


class PlayerCreate(BaseModel):
    player_name: str = PlayerFields.player_name
    avatar_id: int = PlayerFields.avatar_id
    player_state: int = PlayerFields.player_state
    lives: int = PlayerFields.lives

    class Config:
        orm_mode = True


class PlayerRead(PlayerCreate):
    player_id: str = PlayerFields.player_id
    lobby_id: Optional[str] = GameFields.lobby_id
    player_state: int = PlayerFields.player_state

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
