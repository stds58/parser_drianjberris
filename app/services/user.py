from fastapi import HTTPException, status, Header, Request
from app.utils.auth import get_password_hash, create_access_token, authenticate_user, get_current_user
from app.crud.user import UserDAO
from app.schemas.user import SUserRegister, SUserAuth
from app.exceptions.exceptions import UserAlreadyExistsError, IncorrectEmailOrPasswordException
import httpx



class UserService:
    @classmethod
    async def register_user(cls, user_data: SUserRegister) -> dict:
        user = await UserDAO.find_one_or_none(options=None, filters={"email": user_data.email})
        if user:
            raise UserAlreadyExistsError()

        # hashed_password =get_password_hash(user_data.password)
        # await UsersDAO.add(
        #     email=user_data.email,
        #     password=hashed_password,
        #     #другие поля
        # )
        user_dict = user_data.model_dump()
        hashed_password = get_password_hash(user_data.password)
        user_dict['password'] = hashed_password
        await UserDAO.add(**user_dict)
        return {'message': 'Вы успешно зарегистрированы!'}

    @classmethod
    async def get_current_user(cls, request: Request):
        user = request.session.get("user")
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return user

    @classmethod
    async def get_token(cls, authorization: str = Header(...)):
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization type"
            )
        return authorization.split(" ")[1]

    @classmethod
    async def verify_session(cls, token: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "http://localhost:8080/realms/tbcrealm/protocol/openid-connect/userinfo",
                headers={"Authorization": f"Bearer {token}"}
            )
            if resp.status_code != 200:
                raise HTTPException(status_code=401, detail="Session invalidated")
            return resp.json()