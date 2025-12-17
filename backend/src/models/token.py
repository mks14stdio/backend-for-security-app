
from mmap import MAP_POPULATE

from sqlalchemy import ForeignKey
from src.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token: Mapped[str] = mapped_column(primary_key=True)

class TestSessionToken(Base):
    __tablename__ = "test_session_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str]

class TestSessionItem(Base):
    __tablename__ = "test_session_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    test_session_id: Mapped[int] = mapped_column(ForeignKey("test_session_tokens.id", ondelete="CASCADE"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="SET NULL"))
    