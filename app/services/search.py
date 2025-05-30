from app.crud.search import SearchDAO
from app.schemas.search import SSearch, SSearchAdd, SSearchFilter
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError
from fastapi import Request
from fastapi.datastructures import FormData
from fastapi.responses import StreamingResponse
from app.services.parser_worker import run_parser
from app.services.item import find_all_stream_item
import anyio
from app.dependencies.get_db import connection
from fastapi import Depends
from app.db.session import get_session_with_isolation
from app.db.session import async_session_maker
import asyncio


async def find_many_search(filters: SSearchFilter, session: AsyncSession):
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
    phrase = await add_one_search(data=search_data, session=session)
    return phrase

async def add_new_items(session: AsyncSession):
    db_search = await find_many_search(filters=None, session=session)
    await session.close()
    if len(db_search) > 0:
        phrase = db_search[0].phrase
        phrase_id = db_search[0].id

        parser_session = async_session_maker()
        stream_session = async_session_maker()
        async def run_and_save():
            try:
                async for batch in run_parser(phrase_id=phrase_id, phrase=phrase, session=parser_session):
                    pass
            finally:
                await parser_session.close()

        async def stream_from_db():
            await asyncio.sleep(1)
            try:
                async for item in find_all_stream_item(filters=None, session=stream_session):
                    yield item
            finally:
                await stream_session.close()

        try:
            async with anyio.create_task_group() as tg:
                tg.start_soon(run_and_save)

                async for item in stream_from_db():
                    yield item

        except GeneratorExit:
            pass
        finally:
            await parser_session.close()
            await stream_session.close()



