import select
from typing import List

from sqlalchemy import select  # noqa: F811
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.article import Article


class ArticleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def add(self, article: Article) -> Article:
        self.session.add(article)
        await self.session.flush()
        return article

    async def delete(self, article: Article) -> None:
        await self.session.delete(article)

    async def find_all(self, limit: int = 10, offset: int = 0) -> List[Article]:
        stmt = select(Article).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return [i for i in result.scalars().all()]

    async def find(self, id: int) -> Article | None:
        return await self.session.get(Article, id)
