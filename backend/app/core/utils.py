from uuid import uuid4
import random
import string

__all__ = ("get_uuid",)


def get_uuid() -> str:
    return str(uuid4())


def get_lobby_id() -> str:
    random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return random_code
