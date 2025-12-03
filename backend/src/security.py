
from enum import Enum

import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from .settings import settings

class TokenType(Enum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_token(
        payload: dict,
        expires: timedelta,
        token_type: TokenType
) -> str:
    to_encode = payload.copy()
    now = datetime.now(tz=timezone.utc)

    to_encode.update({"exp": now + expires})
    to_encode.update({"iat": now})
    to_encode.update({"type": token_type.value})

    return jwt.encode(to_encode, settings.PRIVATE_KEY_PATH.read_text(), algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.PUBLIC_KEY_PATH.read_text(), algorithms=[settings.JWT_ALGORITHM])
