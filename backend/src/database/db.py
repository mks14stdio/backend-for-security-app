from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings

engine = create_async_engine(settings.DATABASE_URL)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase): ...


async def create_session_db():
    async with async_session() as session:
        yield session


@asynccontextmanager
async def transaction(session: AsyncSession):
    try:
        yield
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=409, detail=f"Conflict: {str(e)}")
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Unknown error: {str(e)}")


SessionDep = Annotated[AsyncSession, Depends(create_session_db)]
