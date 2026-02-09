from fastapi import APIRouter

from src.api.dependecy import GetUser
from src.scheme.user import UserRead

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/me")
async def get_me(user: GetUser) -> UserRead:
    return UserRead.model_validate(user)
