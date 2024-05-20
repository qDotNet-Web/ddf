from pydantic import Field
from ..core.utils import get_uuid
from typing import List

__all__ = ("GameFields", "PlayerFields")

_string = dict(min_length=1)


class GameFields:
    lobby_id = Field(
        description="The unique identifier of the lobby",
        example=get_uuid()
    )
    code = Field(
        description="The unique code for the lobby",
        example="ABC123",
        **_string
    )
    owner_id = Field(
        description="The unique identifier of the lobby owner",
        example=get_uuid()
    )
    owner_name = Field(
        description="The name of the lobby owner",
        example="John Doe",
        **_string
    )
    game_state = Field(
        description="The status of the lobby",
        example=0
    )
    players: List[str] = Field(
        description="The list of players in the lobby",
        example=[],
        default_factory=list
    )
    round_timer = Field(
        description="The time in seconds for each round",
        example=180
    )
    lives_per_player = Field(
        description="The number of lives each player has",
        example=3
    )
    max_players = Field(
        description="The maximum number of players allowed in the lobby",
        example=10
    )
    game_type = Field(
        description="The status of the lobby",
        example=0
    )


class PlayerFields:
    player_id = Field(
        description="The unique identifier of the player",
        example=get_uuid()
    )
    player_name = Field(
        description="The name of the player",
        example="John Doe",
        **_string
    )
    lives = Field(
        description="The number of lives the player has",
        example=3
    )
    is_alive = Field(
        description="The status of the player",
        example=True
    )
    avatar_id = Field(
        description="The id of the avatar",
        example=1
    )
    player_state = Field(
        description="The status of the player",
        example=0
    )


class QuestionFields:
    question_id = Field(
        description="The unique identifier of the question",
        example=get_uuid()
    )
    question = Field(
        description="The question",
        example="What is the capital of Germany?",
        **_string
    )
    answer = Field(
        description="The answer to the question",
        example="Berlin",
        **_string
    )
    used = Field(
        description="The status of the question",
        example=False
    )