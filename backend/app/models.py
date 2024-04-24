from pydantic import BaseModel, Field, UUID4
from typing import Optional, List 
from uuid import uuid4

class Player(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    name: str
    avatar: Optional[str] = None

class Lobby(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    host: Player
    players: List[Player] = []
    is_active: bool = False


