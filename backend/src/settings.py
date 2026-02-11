import warnings
from typing import Literal, Self

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    ENV_TYPE: Literal["local", "dev", "production"] = "local"

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    JWT_PRIVATE_KEY: str = "changethis"
    JWT_PUBLIC_KEY: str = "changethis"

    JWT_ALGORITHM: str = "PS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    QUIZ_QUESTION_MINUTES_PER: int = 2

    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    API_URL: str = "/v1"

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENV_TYPE == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("JWT_PRIVATE_KEY", self.JWT_PRIVATE_KEY)
        self._check_default_secret("JWT_PUBLIC_KEY", self.JWT_PUBLIC_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.DB_PASSWORD)
        self._check_default_secret("FIRST_SUPERUSER_PASSWORD", self.ADMIN_PASSWORD)

        return self


settings = Settings()
