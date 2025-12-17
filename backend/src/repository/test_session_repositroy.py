from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.token import TestSessionItem, TestSessionToken

class TestSessionRepository:
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, token: str) -> TestSessionToken:
        stmt = insert(TestSessionToken).values({"token": token}).returning(TestSessionToken)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()
    
    async def delete_one(self, token: str) -> None:
        stmt = delete(TestSessionToken).where(TestSessionToken.token == token)
        await self.session.execute(stmt)
        await self.session.flush()

    
    async def add_item(self, test_session_pk: int, question_pk: int) -> TestSessionItem:
        stmt = insert(TestSessionItem).values({
            "test_session_id": test_session_pk,
            "question_id": question_pk
        }).returning(TestSessionItem)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()

    async def find_one_by_token(self, token: str) -> TestSessionToken | None:
        stmt = select(TestSessionToken).where(TestSessionToken.token == token)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def find_items_by_session_pk(self, test_session_pk: int) -> list[TestSessionItem]:
        stmt = select(TestSessionItem).where(TestSessionItem.test_session_id == test_session_pk)
        result = await self.session.execute(stmt)
        return [i for i in result.scalars().all()]
    