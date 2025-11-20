import datetime
from datetime import timedelta

import jwt
from fastapi import HTTPException


from starlette import status

from src.scheme.user import UserRead
from src.models.users import User
from src.repository.user_repository import UserRepository
from src.scheme.auth import RefreshSchema
from ..scheme.auth import LoginSchema, TokenInfo
from ..security import verify_password, create_token, TokenType, decode_token


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository: UserRepository = repository


    async def login(self, login: LoginSchema):

        unauthed_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

        user_filters = {"email": login.email}

        if not (user := await self.repository.find_one(**user_filters)):
            raise unauthed_exception

        if not verify_password(
            password=login.password,
            hashed=user.hashed_password
        ):
            raise unauthed_exception

        if not user.is_active:
            raise unauthed_exception

        access_token = create_token({"sub": str(user.id), "role": user.role.value, "email": user.email,
                                     "fullname": user.full_name}, timedelta(minutes=5), TokenType.ACCESS_TOKEN)
        refresh_token = create_token({"sub": str(user.id) }, timedelta(days=30), TokenType.REFRESH_TOKEN)

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
        )


    async def refresh(self, refresh_token: RefreshSchema) -> TokenInfo:

        try:
            decoded_refresh_token = decode_token(refresh_token.refresh_token)
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token")

        user_filters = {"id": int(decoded_refresh_token["sub"])}

        user: User | None = await self.repository.find_one(**user_filters)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User doesnt exist")

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not active")

        access_token = create_token({"sub": str(user.id), "role": user.role.value, "email": user.email,
                                     "fullname": user.full_name}, timedelta(minutes=5), TokenType.ACCESS_TOKEN)
        #new_refresh_token = create_token({"sub": str(user.id) }, timedelta(days=30), TokenType.REFRESH_TOKEN)

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token.refresh_token,
        )
    
    def get_currect_user(self, access_token: str):
        try:
            payload = decode_token(access_token)
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token")
        
        result = UserRead(
            full_name=payload["fullname"],
            is_active=True,
            email=payload["email"],
            role=payload["role"],
        )

        return result
