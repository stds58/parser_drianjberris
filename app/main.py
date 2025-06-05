import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.base_router import v1_router
from app.api.v2.base_router import v2_router
from app.api.auth.base_router import auth_router
from starlette.middleware.sessions import SessionMiddleware
from app.exceptions.exceptions import http_exception_handler,sqlalchemy_error_handler,integrity_error_handler
from app.keycloak.keycloak import KeycloakManager, get_keycloak_manager, User
from sqlalchemy.exc import IntegrityError, SQLAlchemyError



app = FastAPI(debug=settings.DEBUG, title="API", version="0.1.0")

# Для работы с сессиями (OAuth нужен session middleware)
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_MIDDLEWARE_SECRET_KEY)


# Получаем путь к текущему файлу main.py
# CURRENT_FILE = Path(__file__).resolve()
# CURRENT_DIR = CURRENT_FILE.parent
CURRENT_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE)
STATIC_DIR = os.path.join(CURRENT_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Регистрация обработчиков исключений
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)



@app.get("/")
async def redirect_to_frontend():
    return RedirectResponse(url="/frontend/v2/search/add")

app.include_router(v1_router, prefix="/api")
app.include_router(v2_router, prefix="/frontend")
app.include_router(auth_router, prefix="/auth", tags=['auth'])

keycloak_manager = KeycloakManager(keycloak_url="http://localhost:8080", realm="tbcrealm")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=False)
    #python -m cProfile -o output.prof -m uvicorn app.main:app --reload
    # В боевом режиме лучше использовать Gunicorn + Uvicorn workers вместо uvicorn.run(...)
    # https://webadventures.ru/sravnenie-wsgi-serverov-uvicorn-i-gunicorn/