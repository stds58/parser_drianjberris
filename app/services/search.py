import anyio
import asyncio
from fastapi.datastructures import FormData
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.search import SearchDAO
from app.services.parser_worker import run_parser
from app.services.item import find_all_stream_item
from app.schemas.search import SSearch, SSearchAdd, SSearchFilter, SSearchUpdate


async def find_many_search(filters: SSearchFilter, session: AsyncSession):
    searchs = await SearchDAO.find_many(session=session, filters=filters)
    return searchs

async def add_one_search(data: SSearchAdd, session: AsyncSession):
    search = await SearchDAO.add_one(session=session, values=data)
    return search

async def delete_all_search(session: AsyncSession):
    search = await SearchDAO.delete_all(session=session)
    return search

async def add_new_search(data: FormData, session: AsyncSession):
    search_data = SSearchAdd(**dict(data))
    data = {"phrase": search_data.phrase, "is_parsed": False}
    del_db_search = await delete_all_search(session=session)
    phrase = await add_one_search(data=data, session=session)
    return phrase

async def update_one_search(phrase_id: int, session: AsyncSession):
    validated_data = SSearchUpdate(id=phrase_id)
    values = {"is_parsed": True}
    update_data = await SearchDAO.update_one(id=validated_data.id, values=values, session=session)
    return update_data

async def add_new_items(session: AsyncSession,session2: AsyncSession,session3: AsyncSession):
    db_search = await find_many_search(filters=None, session=session)
    await session.close()
    if len(db_search) > 0:
        phrase = db_search[0].phrase
        phrase_id = db_search[0].id

        print('db_search[0].is_parsed ',db_search[0].is_parsed)

        # Проверяем, был ли уже выполнен парсинг
        if db_search[0].is_parsed:
            async def stream_from_db():
                try:
                    async for item in find_all_stream_item(filters=None, session=session3):
                        yield item
                finally:
                    await session3.close()

            async for item in stream_from_db():
                yield item
            return

        parser_session = session2
        stream_session = session3
        async def run_and_save():
            try:
                async for batch in run_parser(phrase_id=phrase_id, phrase=phrase, session=parser_session):
                    if batch == "ok":
                        print("================================================================================")
                        await update_one_search(phrase_id=phrase_id, session=session)
                        break
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



