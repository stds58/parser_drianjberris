from app.crud.item import ItemDAO
from app.schemas.item import SItem, SItemAdd, SItemFilter
from sqlalchemy.ext.asyncio import AsyncSession


async def find_many_item(filters: SItemFilter, session: AsyncSession):
    items = await ItemDAO.find_many(session=session, filters=filters)
    return items

async def find_all_stream_item(filters: SItemFilter, session: AsyncSession):
    rows = ItemDAO.find_all_stream(session=session, filters=filters)
    async for row in rows:
        yield row

async def add_one_item(data: SItemAdd, session: AsyncSession):
    item = await ItemDAO.add_one(session=session, **data.model_dump())
    return item

async def add_many_item(data: SItemAdd, session: AsyncSession):
    item = await ItemDAO.add_many(session=session, values_list=data)
    return item

async def delete_all_item(session: AsyncSession):
    item = await ItemDAO.delete_all(session=session)
    return item

async def find_items_since(last_id: int, session: AsyncSession):
    items = await ItemDAO.find_items_since(last_id=last_id, session=session)
    return items
