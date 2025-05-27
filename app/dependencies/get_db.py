import os
from app.core.config import get_db_url
from contextlib import asynccontextmanager
from functools import wraps
from typing import Optional, Callable, Any, AsyncGenerator
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import HTTPException
from app.db.session import async_session_maker, get_session_with_isolation
import logging


logger = logging.getLogger(__name__)


def connection(isolation_level: Optional[str] = None, commit: bool = True):
    """
    Фабрика зависимости для FastAPI, создающая асинхронную сессию с заданным уровнем изоляции.
    """
    async def dependency() -> AsyncGenerator[AsyncSession, None]:
        async with get_session_with_isolation(async_session_maker, isolation_level) as session:
            try:
                result = await session.execute(text("SHOW transaction_isolation;"))
                print("SHOW transaction_isolation;", result.scalar())
                yield session
                if commit and session.in_transaction():
                    await session.commit()
            except IntegrityError as e:
                if session.in_transaction():
                    await session.rollback()
                await session.rollback()
                raise e # HTTPException(status_code=400, detail=f"Ошибка целостности данных: {e.orig}") from e
            except SQLAlchemyError as e:
                if session.in_transaction():
                    await session.rollback()
                raise e # HTTPException(status_code=500, detail=f"Ошибка БД: {e}") from e
            except Exception as e:
                if session.in_transaction():
                    await session.rollback()
                raise
    return dependency






def connection2(isolation_level: Optional[str] = None, commit: bool = True):
    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            async with async_session_maker() as session:
                try:
                    if isolation_level:
                        await session.execute(text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}"))
                        # Проверяем уровень изоляции
                        result = await session.execute(text("SHOW TRANSACTION ISOLATION LEVEL;"))
                        current_isolation_level = result.scalar()
                        print(f"Текущий уровень изоляции: {current_isolation_level}")
                    result = await method(*args, session=session, **kwargs)
                    if commit:
                        await session.commit()
                    return result
                except IntegrityError as e:
                    logger.error(f"Ошибка целостности данных: {e.orig}")
                    raise HTTPException(status_code=400, detail=f"Ошибка целостности данных: {e.orig}")
                except SQLAlchemyError as e:
                    logger.error(f"Ошибка при работе с базой данных: {e}")
                    raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
                except Exception as e:
                    await session.rollback()
                    raise
                finally:
                    await session.close()
        return wrapper
    return decorator



# """
#     Декоратор для управления сессией с возможностью настройки уровня изоляции и коммита.
#     Параметры:
#     - `isolation_level`: уровень изоляции для транзакции (например, "SERIALIZABLE").
#     - `commit`: если `True`, выполняется коммит после вызова метода.
#     READ COMMITTED — для обычных запросов (по умолчанию в PostgreSQL).
#     SERIALIZABLE — для финансовых операций, требующих максимальной надежности.
#     REPEATABLE READ — для отчетов и аналитики.
#
#     # Чтение данных
#     @connection(isolation_level="READ COMMITTED")
#     async def get_user(self, session, user_id: int):
#         ...
#     # Финансовая операция
#     @connection(isolation_level="SERIALIZABLE", commit=False)
#     async def transfer_money(self, session, from_id: int, to_id: int):
#         ...
#     """