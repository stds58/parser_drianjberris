from typing import Optional, List, Dict, TypeVar, Any, Generic, ClassVar, AsyncGenerator
from fastapi import status
from pydantic import BaseModel as PydanticModel
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select, update  #, insert
from sqlalchemy.dialects.postgresql import insert
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
    async def add_one(cls, session: AsyncSession, values: Dict) -> ModelType:
        new_instance = cls.model(**values)
        session.add(new_instance)
        await session.flush()
        await session.refresh(new_instance)
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, values_list: List[Dict]) -> None:
        stmt = insert(cls.model).values(values_list)
        stmt = stmt.on_conflict_do_nothing()
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

    @classmethod
    async def find_items_since(cls, last_id: int, session: AsyncSession):
        result = await session.execute(
            select(cls.model).where(cls.model.id > last_id).order_by(cls.model.id)
        )
        return result.scalars().all()

    @classmethod
    async def update_one(cls, id: int, values: Dict, session: AsyncSession) -> None:
        stmt = update(cls.model).where(cls.model.id == id).values(values)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def find_one_or_none(cls,
                               session: AsyncSession,
                               filters: FilterSchemaType = None
                               ) -> Optional[ModelType]:
        query = select(cls.model)
        if filters is not None:
            if isinstance(filters, dict):
                filter_dict = filters  # Если filters уже словарь, используем его напрямую
            else:
                # Если filters — это Pydantic-модель, преобразуем её в словарь
                filter_dict = filters.model_dump(exclude_unset=True)
            # filter_dict = filters.model_dump(exclude_unset=True)
            filter_dict = {key: value for key, value in filter_dict.items() if value is not None}
            query = query.filter_by(**filter_dict)
        result = await session.execute(query)
        return result.scalar_one_or_none()






