
from typing import Any, List
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.users import User


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict[str, Any]) -> User:
        print(data)
        stmt = insert(User).values(**data).returning(User)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one()

    async def find_all(self) -> List[User]:
        stmt = select(User)
        res = await self.session.execute(stmt)
        objects = [i for i in res.scalars().all()]
        return objects

    async def find_one(self, **filter_by):
        stmt = select(User).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()