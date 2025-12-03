
from readline import insert_text
from typing import List
from sqlalchemy import insert, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession


from src.models.question import Question, QuestionAnswer

class QuestionRepositroy:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one_question(self, data: dict) -> Question:
        stmt = insert(Question).values(data).returning(Question)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()

    async def add_questions(self, data: List[dict]) -> List[Question]:
        stmt = insert(Question).values(data).returning(Question)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return list(result.scalars().all())
        

    async def update_question(self, id: int, data: dict) -> Question:
        stmt = update(Question).where(Question.id == id).values(data).returning(Question)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()

    async def find_one(self, id: int) -> Question | None:
        stmt = select(Question).where(Question.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_pk_test_random(self, pk_id: int, limit: int) -> List[Question]:
        stmt = select(Question).where(Question.test_pk == pk_id).order_by(func.random()).limit(limit)
        result = await self.session.execute(stmt)
        return [i for i in result.scalars().all()]

    async def add_one_question_answer(self, data: dict) -> QuestionAnswer:
        stmt = insert(QuestionAnswer).values(data).returning(QuestionAnswer)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()
    
    async def update_question_answer(self, id: int, data: dict) -> QuestionAnswer:
        stmt = update(QuestionAnswer).where(QuestionAnswer.id == id).values(data).returning(QuestionAnswer)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()
        
