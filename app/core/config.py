import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

# прочитать .env из соседнего репозитория
# current_dir = os.getcwd()
# # Поднимаемся на уровень выше 2 раза
# project_root = os.path.dirname(os.path.dirname(current_dir))
# dotenv_path = f"{project_root}/devops/.env"
#
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
# else:
#     load_dotenv()
#     #raise FileNotFoundError(f".env file not found at {dotenv_path}")


current_dir = os.path.dirname(os.path.abspath(__file__))  # app/core/
parent_dir = os.path.dirname(current_dir)                 # app/
project_dir = os.path.dirname(parent_dir)                 # fastapi_template/
env_path = os.path.join(project_dir, ".env")
# print(f"пути в проекте\n"
#       f"current_dir {current_dir}\n"
#       f"parent_dir {parent_dir}\n"
#       f"project_dir {project_dir}\n"
#       f"env_path {env_path}")

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
        #env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        env_file=env_path
    )

settings = Settings()

#print(settings.model_dump())

def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


