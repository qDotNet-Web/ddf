from uuid import uuid4
import random

__all__ = ("get_uuid",)


def get_uuid() -> str:
    return str(uuid4())


def get_lobby_id() -> str:
    random_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=8))
    return random_code
