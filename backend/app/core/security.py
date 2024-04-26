from datetime import datetime, timedelta
from jose import jwt
import pytz
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    timezone = pytz.timezone("Europe/Berlin")
    if expires_delta:
        expire = datetime.now(timezone) + expires_delta
    else:
        expire = datetime.now(timezone) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt