"""
        exp = payload.get('exp')
        iat = payload.get('iat')
        auth_time = payload.get('auth_time')

        Основные поля токена
        expiration time Время истечения
            "exp": {datetime.utcfromtimestamp(exp).strftime('%d.%m.%Y %H:%M:%S UTC') if exp else None},

        Issued at время выдачи токена
            "iat": {datetime.utcfromtimestamp(iat).strftime('%d.%m.%Y %H:%M:%S UTC') if iat else None},
            "exp_minutes": {(exp - iat) // 60 if exp and iat else None},

        Время последней аутентификации пользователя.
        Используется для проверки того, что пользователь действительно сам вошёл в систему
            "auth_time": {datetime.utcfromtimestamp(auth_time).strftime('%d.%m.%Y %H:%M:%S UTC') if exp else None},

        Уникальный идентификатор токена (JWT ID), используется для предотвращения повторного использования токена (replay attack)
            "jti ": "{payload.get('jti')}",

        Issuer кто выдал токен (адрес Realm в Keycloak)"
            "iss : "{payload.get('iss')}",

        Audience кому предназначен токен. Например, клиентское приложение или API
            "aud ": "{payload.get('aud')}",

        Subject уникальный идентификатор пользователя в Realm
        Уникальный идентификатор пользователя, не меняется даже при изменении логина или email.
        Используйте его как primary key для привязки к своим таблицам
            "sub ": "{payload.get('sub')}",

        Тип токена. Это Bearer Token — токен, который даёт право на доступ без дополнительных проверок
            "typ ": "{payload.get('typ')}",

        Authorized party клиент, от имени которого был запрошен токен (client_id)
            "azp ": "{payload.get('azp')}",

        Session ID — идентификатор сессии пользователя в Keycloak"
            "sid : "{payload.get('sid')}",

        Authentication Context Class Reference уровень безопасности аутентификации.
        '0' значит минимальная безопасность (например, обычный логин)
            "acr ": "{payload.get('acr')}",

        Информация о пользователе
            "preferred_username": "{payload.get('preferred_username')}",
            "email": "{payload.get('email')}",
            "name": "{payload.get('name')}",
            "given_name": "{payload.get('given_name')}",
            "family_name": "{payload.get('family_name')}",
            "locale": "{payload.get('locale')}",
            'email_verified': "{payload.get('email_verified')}",

        Права и роли
        Роли на уровне Realm'а (глобальные роли).
        Например: offline_access позволяет запрашивать refresh-токены.
            "realm_access": "{payload.get('realm_access')}",

        Роли для конкретного ресурса (account это клиент в Keycloak, связанный с пользователем).
        Разрешает действия вроде просмотра профиля, изменения данных и т.п
            "resource_access": "{payload.get('resource_access')}",

        Какие данные были запрошены при авторизации.
        openid — требуется для OpenID Connect.
        email и profile — добавляют соответствующую информацию о пользователе
            "scope": "{payload.get('scope')}",

        Дополнительно
        Разрешённые источники (CORS), которые могут использовать этот токен.
            "allowed-origins": "{payload.get('allowed-origins')}",
        """

from typing import Optional, Dict
import httpx
from fastapi import HTTPException, Depends, Request, status
from pydantic import BaseModel
from jose import jwt, JWTError
from jwt import PyJWKClient
from app.exceptions.exceptions import TokenExpiredException, NoJwtException, NoUserIdException, ForbiddenException
from app.schemas.jwt_token import UserClaims
from datetime import datetime
import pytz
import time
from app.core.config import settings
import logging


logging.basicConfig(level=logging.INFO)



class KeycloakManager:
    def __init__(self, request: Request):
        self.request = request
        self.token = self.get_token()
        self.realm_public_key = self._fetch_realm_public_key()

    def get_token(self) -> str:
        token = self.request.cookies.get("users_access_token")
        #print('token ',token)
        if token:
            return token
        raise HTTPException(status_code=401, detail="Missing token")

    def _fetch_realm_public_key(self) -> str:
        url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}"
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            return "-----BEGIN PUBLIC KEY-----\n" + response.json()["public_key"] + "\n-----END PUBLIC KEY-----"

    def decode_token(self) -> Dict:
        try:
            # Получаем JWKS
            jwks_client = PyJWKClient(f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs")
            print('self.token ',self.token)
            signing_key = jwks_client.get_signing_key_from_jwt(self.token)

            # Декодируем
            payload = jwt.decode(
                self.token,
                key=signing_key.key,
                algorithms=["RS256"],
                audience="account",
                options={"require_exp": True}
            )
            return payload
        except JWTError as e:
            raise NoJwtException(detail=f"JWT-токен отсутствует или не валиден {e}")

    async def get_user_from_token(self) -> UserClaims:
        logging.info("Получаем токен из заголовка")
        #token = await self.get_token()
        payload = self.decode_token()

        #Проверка истечения срока действия
        if payload['exp'] < int(time.time()):
            raise Exception("Токен истёк")

        #Получение информации о пользователе
        user_info = {
            'username': payload['preferred_username'],
            'email': payload['email'],
            'full_name': payload.get('name'),
            'roles': payload['realm_access']['roles']
        }

        #Проверка ролей
        if 'admin' in payload['realm_access']['roles']:
            print("Пользователь — админ")
        else:
            print("Доступ ограничен")
        print(payload)

        try:
            exp = payload.get('exp')
            iat = payload.get('iat')
            auth_time = payload.get('auth_time')
            payload['exp_gumanize'] = datetime.utcfromtimestamp(exp).strftime('%d.%m.%Y %H:%M:%S UTC') if exp else None
            payload['iat_gumanize'] = datetime.utcfromtimestamp(iat).strftime('%d.%m.%Y %H:%M:%S UTC') if iat else None
            payload['exp_minutes_gumanize'] = (exp - iat) // 60 if exp and iat else None
            payload['auth_time_gumanize'] = datetime.utcfromtimestamp(auth_time).strftime('%d.%m.%Y %H:%M:%S UTC') if exp else None
            return UserClaims(**payload)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid token claims: {e}")



