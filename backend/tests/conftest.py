from multiprocessing.spawn import import_main_path
from venv import create
import pytest
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.main import app
from src.database.db import create_session_db, Base
from src.api.dependecy import get_user

from src.settings import settings as s


from src.models.users import User
from src.models.article import Article
from src.models.module import Module, ModuleItem
from src.models.test import Test
from src.models.question import Question, QuestionAnswer, QuestionType

from src.scheme.auth import UserRole

app.dependency_overrides[get_user] = lambda: {"role": UserRole.ADMIN}

# Создаем отдельную тестовую базу данных
TEST_DATABASE_URL = f"postgresql+asyncpg://{s.DB_USER}:{s.DB_PASSWORD}@{s.DB_HOST}:{s.DB_PORT}/test_db"

@pytest_asyncio.fixture(scope="function", autouse=True)
async def get_db():
    # Создаем базу, если ее нет
    admin_engine = create_async_engine(
        f"postgresql+asyncpg://{s.DB_USER}:{s.DB_PASSWORD}@{s.DB_HOST}:{s.DB_PORT}/postgres",
        isolation_level="AUTOCOMMIT",
    )

    try:
        async with admin_engine.begin() as conn:
            await conn.exec_driver_sql("CREATE DATABASE test_db")
    except Exception:
        pass
    finally:
        await admin_engine.dispose()

    # Подключаемся к тестовой базе
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    test_session = async_sessionmaker(test_engine, expire_on_commit=False)

    # Создаем таблицы
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_db():
        async with test_session() as session:
            yield session

    app.dependency_overrides[create_session_db] = override_db

    yield test_session

    # --- Очистка базы после теста ---
    async with test_engine.begin() as conn:
        # ВАЖНО: выполняем команды отдельно
        await conn.exec_driver_sql("DROP SCHEMA public CASCADE")
        await conn.exec_driver_sql("CREATE SCHEMA public")

    await test_engine.dispose()


    # Удаляем тестовую базу (опционально)
    # admin_engine = create_async_engine(
    #     f"postgresql+asyncpg://{s.DB_USER}:{s.DB_PASSWORD}@{s.DB_HOST}:{s.DB_PORT}/postgres",
    #     isolation_level="AUTOCOMMIT"
    # )
    # async with admin_engine.begin() as conn:
    #     await conn.execute("DROP DATABASE test_db")
    # await admin_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), 
                           base_url="http://test") as ac:
        yield ac
