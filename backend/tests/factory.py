from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session

from src.database.db import Base
from src.models.achievement import Achievement
from src.models.article import Article
from src.models.module import Module


async def push_to_database(db: AsyncSession, model: Base):
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model


async def create_article(db: AsyncSession, **kwargs) -> Article:
    article = Article(
        title=kwargs.get("title", "Test Article"),
        content=kwargs.get("content", "Article Content Test"),
    )

    return await push_to_database(db, article)  # pyright: ignore[reportReturnType]


async def create_module(db: AsyncSession, **kwargs) -> Module:
    module = Module(
        need_to_unlook=kwargs.get("xp", 0),  # FREE
        title=kwargs.get("title", "Module Title"),
    )

    return await push_to_database(db, module)  # pyright: ignore[reportReturnType]


async def create_achievement(db: AsyncSession, **kwargs) -> Achievement:
    achievement = Achievement(
        name=kwargs.get("name", "Achievement Name"),
        description=kwargs.get("description", "The epic achievement"),
        icon=None,
        icon_pk=None,
    )

    return await push_to_database(db, achievement)  # pyright: ignore[reportReturnType]
