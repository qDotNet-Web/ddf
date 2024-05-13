from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    MONGODB_DB_NAME: str = "ddf_db"
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
    REDIS_USER: str = os.getenv("REDIS_USER")
    REDIS_DB: int = os.getenv("REDIS_DB")
    SECRET_KEY: str = os.getenv("SECRET_KEY")


settings = Settings()
