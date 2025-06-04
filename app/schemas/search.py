#модели Pydantic  https://habr.com/ru/companies/amvera/articles/851642/
from typing import Optional, List
from pydantic import Field
from app.schemas.base import BaseConfigModel, BaseFilter


class SSearch(BaseConfigModel):
    id: Optional[int] = None
    phrase: Optional[str] = None
    is_parsed: Optional[bool] = None


class SSearchAdd(BaseConfigModel):
    phrase: str = Field(...)
    #is_parsed: Optional[bool] = None


class SSearchUpdate(BaseConfigModel):
    id: int = Field(...)
    #phrase: str = Field(...)
    #is_parsed: bool = Field(...)


class SSearchFilter(BaseFilter):
    id: Optional[int] = Field(default=None)
    phrase: Optional[str] = Field(default=None)
    is_parsed: Optional[bool] = None



