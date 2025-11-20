from typing import List

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.user_repository import UserRepository

from ..models.users import User
from ..scheme.user import UserCreate, UserRead

from ..security import get_password_hash

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository: UserRepository = repository 


    async def create_user(self, new_user: UserCreate) -> UserRead:
        users = await self.repository.find_one(**{"email": new_user.email})

        if users:
           raise HTTPException(status_code=400, detail="Email already registered")

        model_new_user: User = await self.repository.add_one(new_user.model_dump())
        return UserRead.model_validate(model_new_user)

    async def get_user_by_email(self, email: EmailStr) -> UserRead:
        user = self.repository.find_one(**{"email": email})
        return UserRead.model_validate(user)