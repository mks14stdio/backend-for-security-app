from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    PRIVATE_KEY_PATH: Path = BASE_DIR / 'certs' / 'private-key.pem'
    PUBLIC_KEY_PATH: Path = BASE_DIR / 'certs' / 'public-key.pem'
    JWT_ALGORITHM: str = 'PS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 #TODO: MAKE IT 5 minute
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    TEST_TOKEN_EXPIRE_MUNUTES: int = 15

    API_URL: str = "/v1"

settings = Settings() # type: ignore