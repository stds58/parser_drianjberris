from typing import Optional, List, Dict, TypeVar, Any, Generic, ClassVar, AsyncGenerator
from fastapi import status
from pydantic import BaseModel as PydanticModel
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select, insert
from sqlalchemy.orm import DeclarativeBase
from app.db.base import Base
from app.schemas.item import SItem


assert issubclass(Base, DeclarativeBase)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=PydanticModel)


class FiltrMixin:
    model: type[DeclarativeBase]

    @classmethod
    def _apply_filters(cls, query, filters: FilterSchemaType):
        """игнорирование полей фильтрации, которых нет в модели"""
        allowed_fields = cls.filter_schema.model_fields.keys()
        filter_dict = {
            k: v for k, v in filters.model_dump().items()
            if k in allowed_fields and v is not None
        }
        return query.filter_by(**filter_dict)


class BaseDAO(FiltrMixin, Generic[ModelType, CreateSchemaType, FilterSchemaType]):
    model: ClassVar[type[ModelType]]
    create_schema: ClassVar[type[CreateSchemaType]]
    filter_schema: ClassVar[type[FilterSchemaType]]

    @classmethod
    async def find_many(cls, session: AsyncSession, filters: Optional[FilterSchemaType] = None) -> List[PydanticModel]:
        query = select(cls.model)
        if filters is not None:
            query = cls._apply_filters(query, filters)
        result = await session.execute(query)
        results = result.unique().scalars().all()
        return [cls.pydantic_model.model_validate(obj, from_attributes=True) for obj in results]

    @classmethod
    async def find_all_stream(cls,
                              session: AsyncSession,
                              filters: FilterSchemaType = None
                              ) -> AsyncGenerator[ModelType, None]:
        query = select(cls.model)
        if filters is not None:
            query = cls._apply_filters(query, filters)
        stream = await session.stream_scalars(query)
        async for record in stream:
            item = SItem.model_validate(record)
            yield item.model_dump_json()

    @classmethod
    async def add_one(cls, session: AsyncSession, **values) -> ModelType:
        new_instance = cls.model(**values)
        session.add(new_instance)
        await session.flush()
        await session.refresh(new_instance)
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, values_list: List[Dict]) -> None:
        stmt = insert(cls.model).values(values_list)
        await session.execute(stmt)
        await session.flush()
        await session.commit()

    @classmethod
    async def delete_all(cls, session: AsyncSession) -> dict:
        query = sqlalchemy_delete(cls.model)
        result = await session.execute(query)
        return {
            "status": "success",
            "message": f"{result.rowcount} записей удалено",
            "deleted_count": result.rowcount,
            "http_status": status.HTTP_200_OK,
        }



