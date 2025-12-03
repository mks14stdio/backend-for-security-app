from typing import List

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.scheme.auth import RegisterSchema
from src.repository.user_repository import UserRepository

from ..models.users import User
from ..scheme.user import UserCreate, UserRead, UserRole


from ..security import get_password_hash

class UserService:

    def __init__(self, session: AsyncSession):
        self.repository: UserRepository = UserRepository(session) 
        self.session: AsyncSession = session


    async def create_user(self, new_user: RegisterSchema, role: UserRole = UserRole.USER) -> UserRead:
        
        if await self.repository.find_one_by_email(new_user.email):
           raise HTTPException(status_code=400, detail="Email already registered")
        
        try:
            user_payload = {
                "email": new_user.email,
                "hashed_password": get_password_hash(new_user.password),
                "role": role
            }
            
            user = await self.repository.add_one(user_payload)

            profile = {
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "age": new_user.age,
                "gender": new_user.gender,
                "user_id": user.id
            }
            await self.repository.add_profile_user(profile)
            await self.session.commit()

            return await self.get_user_by_email(new_user.email)
        except Exception as e:
            await self.session.rollback()
            raise e
            


    async def get_user_by_email(self, email: EmailStr) -> UserRead:
        user = await self.repository.find_one_by_email(email)
        return UserRead.model_validate(user)