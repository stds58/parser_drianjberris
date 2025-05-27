from fastapi import APIRouter, Depends
from app.dependencies.get_db import connection
from app.services.search import find_many_search, add_one_search
from app.schemas.search import SSearchFilter, SSearchAdd
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/find")
async def get_search( filters: SSearchFilter = Depends(), session: AsyncSession = Depends(connection()) ):
    """isolation_level:READ COMMITTED, REPEATABLE READ, SERIALIZABLE; commit=False"""
    searchs = await find_many_search(filters=filters, session=session)
    return {"data": searchs}


@router.post("/add")
async def post_search( data: SSearchAdd, session: AsyncSession = Depends(connection()) ):
    search = await add_one_search(data=data, session=session)
    return {"data": search}

