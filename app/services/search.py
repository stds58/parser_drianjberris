from app.crud.search import SearchDAO
from app.schemas.search import SSearch, SSearchAdd, SSearchFilter
from sqlalchemy.ext.asyncio import AsyncSession


async def find_many_search(filters: SSearchFilter, session: AsyncSession):
    # Пример бизнес-логики: проверка прав пользователя, дополнительная обработка
    # if not await check_user_permissions(...):
    #     raise HTTPException(status_code=403, detail="Нет доступа")
    searchs = await SearchDAO.find_many(session=session, filters=filters)
    return searchs

async def add_one_search(data: SSearchAdd, session: AsyncSession):
    search = await SearchDAO.add_one(session=session, **data.model_dump())
    return search

async def delete_one_search(data: SSearchAdd, session: AsyncSession):
    search = await SearchDAO.delete_one(session=session, **data.model_dump())
    return search
