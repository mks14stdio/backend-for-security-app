from math import exp
from typing import Any, List

from pydantic_core import to_json
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.token import RefreshToken
from src.models.users import User, UserProfile


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user

    async def find_all(self) -> List[User]:
        stmt = select(User)
        res = await self.session.execute(stmt)
        objects = [i for i in res.scalars().all()]
        return objects

    async def find(self, id: int) -> User | None:
        return await self.session.get(User, id)

    async def find_by_email(self, email: str) -> User | None:
        stmt = (
            select(User).where(User.email == email).options(selectinload(User.profile))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
