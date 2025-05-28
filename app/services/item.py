from app.crud.item import ItemDAO
from app.schemas.item import SItem, SItemAdd, SItemFilter
from sqlalchemy.ext.asyncio import AsyncSession


async def find_many_item(filters: SItemFilter, session: AsyncSession):
    items = await ItemDAO.find_many(session=session, filters=filters)
    return items

async def add_one_item(data: SItemAdd, session: AsyncSession):
    item = await ItemDAO.add_one(session=session, **data.model_dump())
    return item

async def delete_all_item(data: SItemAdd, session: AsyncSession):
    item = await ItemDAO.delete_all(session=session)
    return item