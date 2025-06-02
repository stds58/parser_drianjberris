"""
    Контекстный менеджер для создания сессии с опциональным уровнем изоляции.Для гибкого управления уровнем изоляции
"""
from app.core.config import get_db_url
from contextlib import asynccontextmanager
from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def get_session_with_isolation(session_factory, isolation_level: Optional[str] = None):
    async with session_factory() as session:
        if isolation_level:
            await session.connection(execution_options={"isolation_level": isolation_level})
            # Проверяем уровень изоляции
            result = await session.execute(text("SHOW TRANSACTION ISOLATION LEVEL;"))
            current_isolation_level = result.scalar()
            #print(f"Текущий уровень изоляции: {current_isolation_level}")
        yield session

