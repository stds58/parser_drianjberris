"""
DeclarativeBase:
    Основной класс для всех моделей, от которого будут наследоваться все таблицы (модели таблиц).
    Эту особенность класса мы будем использовать неоднократно.
AsyncAttrs:
    Позволяет создавать асинхронные модели, что улучшает производительность при работе с асинхронными операциями.
create_async_engine:
    Функция, создающая асинхронный движок для соединения с базой данных по предоставленному URL.
async_sessionmaker:
    Фабрика сессий для асинхронного взаимодействия с базой данных. Сессии используются для выполнения запросов и транзакций.
"""

from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy import func, text, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import String, Boolean, ForeignKey


# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
created_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


