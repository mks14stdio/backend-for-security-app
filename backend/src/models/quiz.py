from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base

if TYPE_CHECKING:
    from src.models.article import Article


class QuizArticle(Base):
    __tablename__ = "quiz_articles"

    id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="RESTRICT"), primary_key=True
    )

    article: Mapped["Article"] = relationship(
        back_populates="quiz", uselist=False, lazy="noload"
    )

    questions: Mapped[list["Question"]] = relationship(
        back_populates="quiz", lazy="joined"
    )

    question_count: Mapped[int] = mapped_column()


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_pk: Mapped[int] = mapped_column(
        ForeignKey("quiz_articles.id", ondelete="CASCADE")
    )

    quiz: Mapped["QuizArticle"] = relationship(
        back_populates="questions", lazy="noload"
    )

    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question", lazy="joined"
    )

    text: Mapped[str]


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_pk: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE")
    )

    question: Mapped["Question"] = relationship(back_populates="answers", lazy="noload")

    text: Mapped[str]
    is_correct: Mapped[bool] = mapped_column(default=False)
