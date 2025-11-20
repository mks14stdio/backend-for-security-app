import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.main import app
from src.database.db import create_session_db, Base

test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
test_session = async_sessionmaker(engine=test_engine)


@pytest.fixture(scope="function")
async def session():
    async with test_session() as s:
        yield s

app.dependency_overrides[create_session_db] = session

from src.models.users import User

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), 
                           base_url="http://test") as ac:
        yield ac

