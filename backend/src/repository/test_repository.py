from typing import List
from sqlalchemy import delete, insert, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import question
from src.models.question import Question, QuestionAnswer
from src.models.test import Test

class TestRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one_test(self, data: dict) -> Test:
        stmt = insert(Test).values(data).returning(Test)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()
    
    async def delete_one_test(self, id: int) -> None:
        stmt = delete(Test).where(Test.id == id)
        await self.session.execute(stmt)
        await self.session.flush()

    async def find_one(self, id: int) -> Test:
        stmt = select(Test).where(Test.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
        
