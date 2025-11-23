
import select
from tkinter import ARC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select

from src.models.article import Article

class ArticleRepository:
    
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def add_one(self, data: dict) -> Article:
        stmt = insert(Article).values(**data).returning(Article)
        result = await self.session.execute(stmt)
        await self.session.commit()

        return result.scalar_one()
    
    async def update_one(self, id: int, data: dict) -> Article:
        stmt = (
            update(Article)
            .where(Article.id == id)
            .values(**data)
            .returning(Article)
        )
        result = await self.session.execute(stmt)
        
        await self.session.commit()

        return result.scalar_one()
    
    async def find_one(self, id: int) -> Article | None:
        stmt = select(Article).where(Article.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()