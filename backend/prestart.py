import asyncio
import os

from src.database.db import async_session
from src.models.users import User, UserProfile
from src.repository.user_repository import UserRepository
from src.scheme.user import UserRole
from src.security import get_password_hash


async def create_admin():
    admin_email: str | None = os.getenv("ADMIN_EMAIL")
    admin_password: str | None = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        print(f"ADMIN EMAIL {admin_email} PASSWORD {admin_password}")
        exit(1)

    admin_hashed = get_password_hash(admin_password)

    async with async_session() as session:
        repository: UserRepository = UserRepository(session)
        user = await repository.find_by_email(admin_email)

        if user:
            print("Admin alredy exsist")
            exit(0)

        user = User()
        user.email = admin_email
        user.hashed_password = admin_hashed
        user.profile = UserProfile()
        user.profile.first_name = "Denis"
        user.profile.last_name = "Sova"

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
