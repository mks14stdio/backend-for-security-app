from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base
import enum

class QuestionType(enum.Enum):
    single = "single"
    multiple = "multiple"
    text = "text"

class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[QuestionType]
    text: Mapped[str]
    answers: Mapped[List["QuestionAnswer"]] = relationship(back_populates="question", lazy="selectin")

    test: Mapped["Test"] = relationship(back_populates="questions") # type: ignore
    test_pk: Mapped[int] = mapped_column(ForeignKey("tests.id", ondelete="CASCADE"))

class QuestionAnswer(Base):
    __tablename__ = "questionsanswers"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    is_correct: Mapped[bool]

    question: Mapped["Question"] = relationship(back_populates="answers")
    question_pk: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))