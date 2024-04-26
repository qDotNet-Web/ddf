from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    MONGODB_DB_NAME: str = "ddf_db"


settings = Settings()
