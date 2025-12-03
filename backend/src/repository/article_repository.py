
import select
from typing import List

from httpx import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, delete

from src.models import article
from src.models.article import Article

class ArticleRepository:
    
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def add_one(self, data: dict) -> Article:
        stmt = insert(Article).values(**data).returning(Article)
        result = await self.session.execute(stmt)
        await self.session.flush()

        return result.scalar_one()

    async def update_one(self, id: int, data: dict) -> Article:
        stmt = (
            update(Article)
            .where(Article.id == id)
            .values(**data)
            .returning(Article)
        )
        result = await self.session.execute(stmt)
        
        await self.session.flush()
        return result.scalar_one()
    
    async def delete_article(self, id: int) -> None:
        stmt = delete(Article).where(Article.id == id)
        await self.session.execute(stmt)
        await self.session.flush()

    async def find_all(self, limit: int = 10, offset: int = 0) -> List[Article]:
        stmt = select(Article).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return [i for i in result.scalars().all()]
    

    async def find_one(self, id: int) -> Article | None:
        return await self.session.get(Article, id)