
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from src.models.article import Article

class ArticleRepository:
    
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def add_one(self, data: dict, user_id: int) -> Article | None:
        
        stmt = insert(Article).values(**data).returning(Article)
        result = await self.session.execute(stmt)
        
        await self.session.commit()

        return Article()