from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token: Mapped[str] = mapped_column(primary_key=True)
