from sqlalchemy import ForeignKey
from src.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token: Mapped[str] = mapped_column(primary_key=True)

class TestSessionToken(Base):
    __tablename__ = "test_session_tokens"

    token: Mapped[str] =  mapped_column(primary_key=True)

class TestSessionItem(Base):
    __tablename__ = "test_session_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    test_session_token: Mapped[str] = mapped_column(ForeignKey("test_session_tokens.token", ondelete="CASCADE"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="SET NULL"))