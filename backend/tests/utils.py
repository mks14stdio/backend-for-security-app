from httpx import AsyncClient
from tests.conftest import client
from src.scheme.user import UserRegister

async def create_user(*, name: str, password: str, email: str) -> UserRegister:
    return UserRegister(
        full_name=name, password=password, email=email
    )

