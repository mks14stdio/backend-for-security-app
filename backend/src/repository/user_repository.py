
from math import exp
from typing import Any, List
from pydantic_core import to_json
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.token import RefreshToken
from src.models.users import User, UserProfile


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_refresh_token(self, refresh_token: str) -> RefreshToken:

        token = RefreshToken(token=refresh_token)
        self.session.add(token)
        await self.session.commit()
        await self.session.refresh(token)
        return token
    
    async def delete_refresh_token(self, refresh_token: str) -> bool:
        try:
            token = await self.session.get(RefreshToken, refresh_token)
            await self.session.delete(token)
            await self.session.flush()
            await self.session.commit()
        except Exception as e:
            return False
        
        return True

    async def add_one(self, data: dict[str, Any]) -> User:
        stmt = insert(User).values(**data).returning(User)
        res = await self.session.execute(stmt)
        await self.session.flush()
        return res.scalar_one()
    
    async def add_profile_user(self, profile_data: dict[str, Any]) -> UserProfile:
        stmt = insert(UserProfile).values(**profile_data).returning(UserProfile)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()

    async def find_all(self) -> List[User]:
        stmt = select(User)
        res = await self.session.execute(stmt)
        objects = [i for i in res.scalars().all()]
        return objects

    async def find_one(self, id: int) -> User | None:
        stmt = select(User).where(User.id == id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
    
    async def find_one_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email).options(selectinload(User.profile))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()