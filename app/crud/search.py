from app.crud.base import BaseDAO
from app.models.search import Search
from app.schemas.search import SSearch, SSearchFilter, SSearchAdd


class SearchDAO(BaseDAO[Search, SSearchAdd, SSearchFilter]):
    model = Search
    create_schema = SSearchAdd
    filter_schema = SSearchFilter
    pydantic_model = SSearch
