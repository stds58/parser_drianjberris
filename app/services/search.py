from app.crud.search import SearchDAO
from app.schemas.search import SSearch, SSearchAdd, SSearchFilter
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError
from fastapi import Request
from fastapi.datastructures import FormData
from fastapi.responses import StreamingResponse



async def find_many_search(filters: SSearchFilter, session: AsyncSession):
    # Пример бизнес-логики: проверка прав пользователя, дополнительная обработка
    # if not await check_user_permissions(...):
    #     raise HTTPException(status_code=403, detail="Нет доступа")
    searchs = await SearchDAO.find_many(session=session, filters=filters)
    return searchs

async def add_one_search(data: SSearchAdd, session: AsyncSession):
    search = await SearchDAO.add_one(session=session, **data.model_dump())
    return search

async def delete_all_search(session: AsyncSession):
    search = await SearchDAO.delete_all(session=session)
    return search

async def add_new_search(data: FormData, session: AsyncSession):
    search_data = SSearchAdd(**dict(data))
    del_db_search = await delete_all_search(session=session)
    add_db_search = await add_one_search(data=search_data, session=session)
    return data



