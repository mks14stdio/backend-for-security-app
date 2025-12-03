from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings

engine = create_async_engine(settings.DATABASE_URL)

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    ...

async def create_session_db():
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(create_session_db)]
