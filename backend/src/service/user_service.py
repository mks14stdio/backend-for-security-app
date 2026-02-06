from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.user_repository import UserRepository
from src.scheme.auth import RegisterSchema

from ..models.users import User, UserProfile
from ..scheme.user import UserRead, UserRole
from ..security import get_password_hash


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository: UserRepository = UserRepository(session)
        self.session: AsyncSession = session

    async def create_user(
        self, new_user: RegisterSchema, role: UserRole = UserRole.USER
    ) -> UserRead:
        if await self.repository.find_by_email(new_user.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        try:
            hashed_password = get_password_hash(new_user.password)
            user = User(
                hashed_password=hashed_password, email=new_user.email, role=role
            )

            user.profile = UserProfile(
                first_name=new_user.first_name,
                last_name=new_user.last_name,
                age=new_user.age,
                gender=new_user.gender,
            )

            await self.repository.add(user)

            await self.session.commit()
            await self.session.refresh(user)

            return UserRead.model_validate(user)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_user_by_email(self, email: EmailStr) -> UserRead:
        user = await self.repository.find_by_email(email)
        return UserRead.model_validate(user)
