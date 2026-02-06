from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

if TYPE_CHECKING:
    from .module import ModuleItem
    from .quiz import QuizArticle


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()

    module_item: Mapped["ModuleItem"] = relationship(
        back_populates="article", uselist=False, lazy="noload"
    )

    quiz: Mapped["QuizArticle"] = relationship(
        back_populates="article", uselist=False, lazy="select"
    )

    created_on: Mapped[datetime] = mapped_column(default=func.now())
    updated_on: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
