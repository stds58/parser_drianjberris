from typing import Optional, Callable, Any, AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
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
                # result = await session.execute(text("SHOW transaction_isolation;"))
                # print("SHOW transaction_isolation;", result.scalar())
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
            except (ConnectionRefusedError, OSError, OperationalError) as e:
                # Обработка ошибок подключения к БД
                raise e
            except Exception as e:
                if session.in_transaction():
                    await session.rollback()
                raise
    return dependency
