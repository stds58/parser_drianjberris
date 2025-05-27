from fastapi import APIRouter, Depends
from app.dependencies.get_db import connection
from app.services.item import find_many_item, add_one_item
from app.schemas.item import SItemFilter, SItemAdd
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/find")
async def get_item( filters: SItemFilter = Depends(), session: AsyncSession = Depends(connection()) ):
    items = await find_many_item(filters=filters, session=session)
    return {"data": items}


@router.post("/add")
async def post_item( data: SItemAdd, session: AsyncSession = Depends(connection()) ):
    item = await add_one_item(data=data, session=session)
    return {"data": item}