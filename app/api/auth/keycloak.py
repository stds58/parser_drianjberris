from pathlib import Path
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from app.exceptions.exceptions import IncorrectEmailOrPasswordException
from app.utils.auth import get_password_hash, create_access_token, authenticate_user, get_current_user
from app.crud.user import UserDAO
from app.models.user import User
from app.schemas.user import SUserRegister, SUserAuth
from app.dependencies.get_current_admin import get_current_admin_user
from app.services.user import UserService
from app.core.config import settings
from urllib.parse import quote_plus
import os
import requests
import json
import httpx


V2_DIR = Path(__file__).resolve().parent
#V2_DIR = os.path.dirname(os.path.abspath(__file__))
API_DIR = V2_DIR.parent
APP_DIR = API_DIR.parent
TEMPLATES_DIR = APP_DIR / "templates"

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)

oauth = OAuth()

oauth.register(
    name='keycloak',
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret=settings.KEYCLOAK_CLIENT_SECRET,
    server_metadata_url=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/.well-known/openid-configuration",
    redirect_uri=f"{settings.FRONT_URL}/auth/callback/",
    client_kwargs={'scope': 'openid profile email'}
)
# Настройка Keycloak
KEYCLOAK_URL = settings.KEYCLOAK_URL
KEYCLOAK_REALM = settings.KEYCLOAK_REALM
KEYCLOAK_CLIENT_ID = settings.KEYCLOAK_CLIENT_ID
KEYCLOAK_CLIENT_SECRET = settings.KEYCLOAK_CLIENT_SECRET # удалить, если Access Type = public
KEYCLOAK_ADMIN = settings.KEYCLOAK_ADMIN
KEYCLOAK_ADMIN_PASSWORD = settings.KEYCLOAK_ADMIN_PASSWORD
MASTER_REALM = "master"


@router.get("/login/")
async def login_oauth(request: Request):
    redirect_uri = request.url_for("auth_callback")
    print('redirect_uri ',redirect_uri)
    try:
        return await oauth.keycloak.authorize_redirect(request, redirect_uri)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка OAuth: {e}")

@router.get("/htmllogin")
async def login_oauth_page(request: Request):
    return templates.TemplateResponse("login_oauth.html", {"request": request})

@router.get("/callback/")
async def auth_callback(request: Request):
    try:
        token = await oauth.keycloak.authorize_access_token(request)
        user_info = token.get('userinfo')  # данные пользователя из Keycloak
        access_token = token['access_token']
        request.session["user"] = dict(user_info)
        request.session["access_token"] = access_token

        # Восстанавливаем URL, откуда пришёл пользователь
        next_url = request.session.pop("redirect_after_login", "/frontend/v2/user/me/")
        # Создаем ответ и устанавливаем куки
        response = RedirectResponse(url=next_url)
        response.set_cookie(key="users_access_token", value=access_token, httponly=True, path="/")
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка аутентификации: {e}")


@router.get("/logout/")
async def logout_user(request: Request, response: Response):
    response.delete_cookie("users_access_token")
    request.session.clear()
    post_logout_redirect_uri = f"{settings.FRONT_URL}/auth/htmllogin"
    keycloak_logout_url = (
        f"{settings.KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/logout?"
        f"post_logout_redirect_uri={post_logout_redirect_uri}&client_id={KEYCLOAK_CLIENT_ID}"
    )
    return RedirectResponse(url=keycloak_logout_url)



async def verify_keycloak_token(request: Request):
    access_token = request.session.get("access_token")
    if not access_token:
        # Нет токена → редирект на логин
        request.session["redirect_after_login"] = str(request.url)
        raise HTTPException(
            status_code=307,
            detail="Missing token",
            headers={"Location": "/pages/login"}
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8080/realms/tbcrealm/protocol/openid-connect/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        #print('access_token ',access_token)
        #print('response ',response)
        if response.status_code != 200:
            # Токен недействителен → очищаем сессию и редиректим
            request.session.clear()
            request.session["redirect_after_login"] = str(request.url)
            raise HTTPException(
                status_code=307,
                detail="Token invalid or expired",
                headers={"Location": "/pages/login"}
            )

        user_info = response.json()
        request.session["user"] = user_info
        return user_info




