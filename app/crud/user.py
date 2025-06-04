from app.crud.base import BaseDAO
from app.models.user import User
from app.schemas.user import SUserRegister, SUserAuth


class UserDAO(BaseDAO[SUserRegister, SUserRegister, SUserAuth]):
    model = User
    create_schema = SUserRegister
    filter_schema = SUserAuth
    pydantic_model = SUserRegister


