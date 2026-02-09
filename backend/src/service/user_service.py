from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import transaction
from src.exception import UserAlreadyExists
from src.repository.user_repository import UserRepository
from src.scheme.auth import RegisterSchema

from ..models.users import User, UserProfile
from ..scheme.user import UserRole
from ..security import get_password_hash


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository: UserRepository = UserRepository(session)
        self.session: AsyncSession = session

    async def create_user(
        self, new_user: RegisterSchema, role: UserRole = UserRole.USER
    ) -> User:
        if await self.repository.find_by_email(new_user.email):
            raise UserAlreadyExists()

        hashed_password = get_password_hash(new_user.password)
        user = User(hashed_password=hashed_password, email=new_user.email, role=role)

        user.profile = UserProfile(
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            age=new_user.age,
            gender=new_user.gender,
        )

        async with transaction(self.session):
            await self.repository.add(user)
        await self.session.refresh(user)

        return user

    async def get_user_by_email(self, email: EmailStr) -> User | None:
        user = await self.repository.find_by_email(email)
        return user
