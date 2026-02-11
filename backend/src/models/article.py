from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import mapped_collection

from src.database.db import Base

if TYPE_CHECKING:
    from .module import ModuleItem
    from .quiz import QuizArticle


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(256))
    content: Mapped[str] = mapped_column()

    module_item: Mapped["ModuleItem"] = relationship(
        back_populates="article", uselist=False, lazy="noload"
    )

    quiz: Mapped["QuizArticle | None"] = relationship(
        back_populates="article", uselist=False, lazy="selectin"
    )

    created_on: Mapped[datetime] = mapped_column(default=func.now())
    updated_on: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )


class UserArticleCompletion(Base):
    __tablename__ = "user_article_completions"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True
    )

    completed_at: Mapped[datetime] = mapped_column(default=func.now())
