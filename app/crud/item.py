from app.crud.base import BaseDAO
from app.models.item import Item
from app.schemas.item import SItem, SItemFilter, SItemAdd


class ItemDAO(BaseDAO[Item, SItemAdd, SItemFilter]):
    model = Item
    create_schema = SItemAdd
    filter_schema = SItemFilter
    pydantic_model = SItem