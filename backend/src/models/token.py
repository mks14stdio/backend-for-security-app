
from src.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token: Mapped[str] = mapped_column(primary_key=True)

class TestSessionToken(Base):
    __tablename__ = "test_session_tokens"

    token: Mapped[str] = mapped_column(primary_key=True)