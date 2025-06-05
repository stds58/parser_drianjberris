from fastapi import Request, HTTPException, status, Depends
from passlib.context import CryptContext
from jose import jwt, JWTError
from jose.jwk import RSAKey
from jwt import PyJWKClient
from datetime import datetime, timedelta, timezone
from app.core.config import get_auth_data
from app.exceptions.exceptions import TokenExpiredException, NoJwtException, NoUserIdException, ForbiddenException
from app.crud.user import UserDAO
from pydantic import BaseModel, EmailStr



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=1) #timedelta(minutes=1)   timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(filters={"email": email})
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token

from app.core.config import settings
KEYCLOAK_URL = settings.KEYCLOAK_URL
KEYCLOAK_REALM = settings.KEYCLOAK_REALM


async def get_current_user(token: str = Depends(get_token)):
    try:
        TOKEN = token

        # Получаем JWKS
        jwks_client = PyJWKClient(f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs")
        signing_key = jwks_client.get_signing_key_from_jwt(TOKEN)

        # Декодируем
        payload = jwt.decode(
            TOKEN,
            key=signing_key.key,
            algorithms=["RS256"],
            audience="account",
            options={"require_exp": True}
        )
        print("payload ",payload)
    except JWTError as e:
        raise NoJwtException(detail=f"JWT-токен отсутствует или не валиден {e}")

    return payload


