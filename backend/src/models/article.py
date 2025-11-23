from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]
    content: Mapped[str]
    
    test_pk: Mapped[int | None] = mapped_column(ForeignKey("tests.id"))

    created_on: Mapped[datetime] = mapped_column(default=func.now())
    updated_on: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
