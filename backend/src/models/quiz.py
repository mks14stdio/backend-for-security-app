from typing import TYPE_CHECKING, List

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base
from src.scheme.quiz import AnswerType

if TYPE_CHECKING:
    from src.models.article import Article


class QuizArticle(Base):
    __tablename__ = "quiz_articles"

    id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="RESTRICT"), primary_key=True
    )

    xp: Mapped[int] = mapped_column(default=1000)

    article: Mapped["Article"] = relationship(
        back_populates="quiz", uselist=False, lazy="noload"
    )

    questions: Mapped[list["Question"]] = relationship(
        back_populates="quiz", lazy="joined", cascade="all, delete-orphan"
    )

    question_count: Mapped[int] = mapped_column()


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_pk: Mapped[int] = mapped_column(
        ForeignKey("quiz_articles.id", ondelete="CASCADE")
    )

    type: Mapped[AnswerType] = mapped_column(Enum(AnswerType))

    quiz: Mapped["QuizArticle"] = relationship(
        back_populates="questions", lazy="noload"
    )

    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question", lazy="joined", cascade="all, delete-orphan"
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


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    token: Mapped[str] = mapped_column(primary_key=True)
    question_count: Mapped[int]

    article_pk: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE")
    )

    questions: Mapped[List["QuizAttemptQuestion"]] = relationship(
        back_populates="quiz_attempt",
        uselist=True,
        lazy="joined",
        cascade="all, delete-orphan",
    )


class QuizAttemptQuestion(Base):
    __tablename__ = "quiz_attempt_questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_attempt_pk: Mapped[str] = mapped_column(
        ForeignKey("quiz_attempts.token", ondelete="CASCADE")
    )
    question_pk: Mapped[int] = mapped_column(ForeignKey("questions.id"))

    order_index: Mapped[int]

    quiz_attempt: Mapped["QuizAttempt"] = relationship(
        back_populates="questions", lazy="noload"
    )

    __table_args__ = (UniqueConstraint("quiz_attempt_pk", "order_index"),)
