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
from app.keycloak.keycloak import KeycloakManager



V2_DIR = Path(__file__).resolve().parent
API_DIR = V2_DIR.parent
APP_DIR = API_DIR.parent
TEMPLATES_DIR = APP_DIR / "templates"

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# @router.get("/me/")
# async def get_me(user_data: User = Depends(get_current_user)):
#     return user_data

from app.core.config import settings
KEYCLOAK_URL = settings.KEYCLOAK_URL
KEYCLOAK_REALM = settings.KEYCLOAK_REALM

@router.get("/me/")
async def get_me(request: Request):
    xx = KeycloakManager(keycloak_url=KEYCLOAK_URL, realm=KEYCLOAK_REALM)
    yy = await xx.get_user_from_token(request=request)
    return yy
# @router.get("/all_users/")
# async def get_all_users(user_data: User = Depends(get_current_admin_user)):
#     return await UserDAO.find_all()


@router.get("/me-session")
async def test_session(request: Request):
    request.session["test"] = "session_data"
    return {"session": request.session}





