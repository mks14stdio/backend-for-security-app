from datetime import timedelta

import jwt
from fastapi import HTTPException
from starlette import status

from src.exception import AuthTokenError, NotFound
from src.models.token import RefreshToken
from src.models.users import User
from src.repository.refresh_token_repository import RefreshTokenRepository
from src.repository.user_repository import UserRepository
from src.scheme.auth import RefreshSchema
from src.settings import settings

from ..scheme.auth import LoginSchema, TokenInfo
from ..security import TokenType, create_token, decode_token, verify_password


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
    ):
        self.user_repository: UserRepository = user_repository
        self.token_refresh_repository: RefreshTokenRepository = refresh_token_repository

    async def login(self, login: LoginSchema):
        unauthed_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

        if not (user := await self.user_repository.find_by_email(login.email)):
            raise unauthed_exception

        if not verify_password(password=login.password, hashed=user.hashed_password):
            raise unauthed_exception

        if not user.is_active:
            raise unauthed_exception

        access_token = create_token(
            {
                "sub": user.email,
                "role": user.role.value,
            },
            timedelta(minutes=5),
            TokenType.ACCESS_TOKEN,
        )
        refresh_token = create_token(
            {"sub": user.email}, timedelta(days=30), TokenType.REFRESH_TOKEN
        )

        await self.token_refresh_repository.add(RefreshToken(token=refresh_token))

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh(self, refresh_token: RefreshSchema) -> TokenInfo:
        try:
            decoded_refresh_token = decode_token(refresh_token.refresh_token)
        except jwt.InvalidTokenError as e:
            raise AuthTokenError(e)

        if decoded_refresh_token["type"] != TokenType.REFRESH_TOKEN.value:
            raise AuthTokenError()

        founded_refresh_token: (
            RefreshToken | None
        ) = await self.token_refresh_repository.get(refresh_token.refresh_token)

        founded_user: User | None = await self.user_repository.find_by_email(
            decoded_refresh_token["sub"]
        )

        if not founded_refresh_token or not founded_user:
            raise AuthTokenError()

        if not founded_user.is_active:
            raise NotFound(detail="Пользователь не активен")

        await self.token_refresh_repository.delete(founded_refresh_token)

        access_token = create_token(
            {
                "sub": founded_user.email,
                "role": founded_user.role.value,
            },
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            TokenType.ACCESS_TOKEN,
        )
        new_refresh_token = create_token(
            {"sub": founded_user.email},
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            TokenType.REFRESH_TOKEN,
        )

        await self.token_refresh_repository.add(RefreshToken(token=new_refresh_token))

        return TokenInfo(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )

    async def get_currect_user(self, access_token: str) -> User:
        try:
            payload: dict[str, str] = decode_token(access_token)
        except jwt.InvalidTokenError as e:
            raise AuthTokenError(e)

        if payload["type"] != TokenType.ACCESS_TOKEN.value:
            raise AuthTokenError(Exception(f"TokenType is {payload['type']}"))

        user: User | None = await self.user_repository.find_by_email(payload["sub"])

        if not user:
            raise AuthTokenError()

        return user
