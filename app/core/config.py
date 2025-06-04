import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))  # app/core/
parent_dir = os.path.dirname(current_dir)                 # app/
project_dir = os.path.dirname(parent_dir)                 # fastapi_template/
env_path = os.path.join(project_dir, ".env")


class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    ENV: str
    SECRET_KEY: str
    ALGORITHM: str
    SESSION_MIDDLEWARE_SECRET_KEY: str

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=env_path
    )

settings = Settings()


def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


