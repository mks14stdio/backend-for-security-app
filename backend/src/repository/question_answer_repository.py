from typing import List
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.question import Question, QuestionAnswer

class QuestionAnswerRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, data: dict) -> QuestionAnswer:
        stmt = insert(QuestionAnswer).values(data).returning(QuestionAnswer)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()
    
    async def add_all(self, data: List[dict]) -> List[QuestionAnswer]:
        stmt = insert(QuestionAnswer).values(data).returning(QuestionAnswer)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return list(result.scalars().all())
        
