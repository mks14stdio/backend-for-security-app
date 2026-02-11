from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from src.api.dependecy import AuthServiceDep, UserServiceDep
from src.exception import AuthTokenError
from src.scheme.auth import LoginSchema, RefreshSchema, RegisterSchema, TokenInfo
from src.scheme.user import UserRead

router = APIRouter(tags=["Auth"])


@router.post("/login/", summary="Логин")
async def login(auth_service: AuthServiceDep, login: LoginSchema) -> TokenInfo:
    return await auth_service.login(login)


@router.post("/refresh/", summary="Обновление токена")
async def refresh(refresh_token: RefreshSchema, auth_service: AuthServiceDep):
    try:
        return await auth_service.refresh(refresh_token)
    except AuthTokenError as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/register/", summary="Регистрация")
async def register(new_user: RegisterSchema, user_service: UserServiceDep) -> UserRead:
    return UserRead.model_validate(await user_service.create_user(new_user))
