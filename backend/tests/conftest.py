import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.main import app
from src.database.db import create_session_db, Base




from src.models.users import User
from src.models.article import Article
from src.models.module import Module, ModuleItem
from src.models.test import Test
from src.models.question import Question, QuestionAnswer, QuestionType

@pytest.fixture
async def get_db():
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    test_session = async_sessionmaker(engine=test_engine)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_db():
        async with test_session() as session:
            yield session

    app.dependency_overrides[create_session_db] = override_db


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), 
                           base_url="http://test") as ac:
        yield ac

