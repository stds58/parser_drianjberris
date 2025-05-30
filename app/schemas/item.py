from typing import Optional, List
from pydantic import Field
from app.schemas.base import BaseConfigModel, BaseFilter


class SItem(BaseConfigModel):
    id: Optional[int] = None
    id_search: Optional[int] = None
    name: Optional[str] = None
    brand: Optional[str] = None
    price_u: Optional[float] = None
    sale_price_u: Optional[float] = None
    feedbacks: Optional[int] = None
    rating: Optional[int] = None


class SItemAdd(BaseConfigModel):
    id_search: int = Field(...)
    name: str = Field(...)
    brand: str = Field(...)
    price_u: float = Field(...)
    sale_price_u: float = Field(...)
    feedbacks: int = Field(...)
    rating: int = Field(...)


class SItemFilter(BaseFilter):
    id: Optional[int] = None
    id_search: Optional[int] = None
    name: Optional[str] = None
    brand: Optional[str] = None
    price_u: Optional[float] = None
    sale_price_u: Optional[float] = None
    feedbacks: Optional[int] = None
    rating: Optional[int] = None
