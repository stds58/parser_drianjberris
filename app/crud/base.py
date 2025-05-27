from datetime import datetime
from typing import Optional, List, Dict, TypeVar, Any, Generic, ClassVar, AsyncGenerator
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload, class_mapper, declarative_base, DeclarativeBase
from fastapi import HTTPException
from pydantic import BaseModel as PydanticModel
from app.db.base import Base


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
        return result.scalars().all()

    @classmethod
    async def add_one(cls, session: AsyncSession, **values) -> ModelType:
        new_instance = cls.model(**values)
        session.add(new_instance)
        await session.flush()
        await session.refresh(new_instance)
        return new_instance

    @classmethod
    async def delete_one(cls, session: AsyncSession, id: int) -> dict:
        query = sqlalchemy_delete(cls.model).filter_by(id=id)
        result = await session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Объект с ID {id} не найден")
        return {"message": f"Объект с id {id} удален!", "deleted_count": result.rowcount}


