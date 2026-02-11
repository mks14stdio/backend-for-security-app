import asyncio
import os

from src.database.db import async_session
from src.models.users import User, UserProfile
from src.repository.user_repository import UserRepository
from src.scheme.user import UserRole
from src.security import get_password_hash
from src.settings import settings


async def create_admin():

    admin_hashed = get_password_hash(settings.ADMIN_PASSWORD)

    async with async_session() as session:
        repository: UserRepository = UserRepository(session)
        user = await repository.find_by_email(settings.ADMIN_EMAIL)

        if user:
            print("Admin alredy exsist")
            exit(0)

        user = User()
        user.email = settings.ADMIN_EMAIL
        user.hashed_password = admin_hashed
        user.profile = UserProfile()
        user.profile.first_name = "Admin"
        user.profile.last_name = "Admin"

        try:
            await repository.add(user)
            await session.commit()
        except Exception as e:
            print(e)
            await session.rollback()
            exit(1)


def main():
    asyncio.run(create_admin())


if __name__ == "__main__":
    main()
