from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DB_USER: str = "user_dev"
    DB_PASSWORD: str = "qweasdzxc123"
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "test_dev"

    ENV_TYPE: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "private-key.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "public-key.pem"
    JWT_ALGORITHM: str = "PS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int  # Зависит от окружения
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    QUIZ_QUESTION_MINUTES_PER: int = 2

    API_URL: str = "/v1"


settings = Settings()  # pyright: ignore[reportCallIssue]
