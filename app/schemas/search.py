#модели Pydantic  https://habr.com/ru/companies/amvera/articles/851642/
from typing import Optional, List
from pydantic import Field
from app.schemas.base import BaseConfigModel, BaseFilter


class SSearch(BaseConfigModel):
    id: Optional[int] = None
    phrase: Optional[str] = None


class SSearchAdd(BaseConfigModel):
    phrase: str = Field(...)


class SSearchFilter(BaseFilter):
    id: Optional[int] = Field(default=None)
    phrase: Optional[str] = Field(default=None)



