import asyncio
import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.repository.user_repository import UserRepository
from src.scheme.user import UserCreate, UserRole
from src.security import get_password_hash

from src.database.db import async_session

async def create_admin():
    admin_email: str | None = os.getenv("ADMIN_EMAIL")
    admin_password: str | None = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        print(f"ADMIN EMAIL {admin_email} PASSWORD {admin_password}")
        exit(1)

    admin_hashed = get_password_hash(admin_password)

    admin_create = UserCreate(full_name="Admin", hashed_password=admin_hashed, role=UserRole.ADMIN, email=admin_email)

    async with async_session() as session:
        repository: UserRepository = UserRepository(session)
        user = await repository.find_one(**{"email": admin_email})

        if user:
            print("EMAIL EXISTS")
            exit(1)
        
        await repository.add_one(admin_create.model_dump())


    



def main():
    asyncio.run(create_admin())

if __name__ == "__main__":
    main()