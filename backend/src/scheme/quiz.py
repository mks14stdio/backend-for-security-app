import enum
from typing import Self

from pydantic import BaseModel, model_validator
from pydantic.fields import Field


class AnswerType(str, enum.Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"
    SELECTABLE = "selectable"


class AnswerCreate(BaseModel):
    text: str
    is_correct: bool


class AnswerRead(BaseModel):
    text: str
    is_correct: bool

    model_config = {"from_attributes": True}


class QuestionCreate(BaseModel):
    text: str
    type: AnswerType
    answers: list[AnswerCreate]


class QuestionRead(BaseModel):
    text: str
    type: AnswerType
    answers: list[AnswerRead]

    model_config = {"from_attributes": True}


class QuizCreate(BaseModel):
    question_count: int = Field(..., ge=1)
    questions: list[QuestionCreate]

    @model_validator(mode="after")
    def check_questions_more(self) -> Self:
        if self.question_count <= 3 and len(self.questions) <= 3:
            raise ValueError("Кол-во вопросов должно быть больше 3")

        if self.question_count > len(self.questions):
            raise ValueError("Кол-во вопросов больше чем общее кол-во вопросов")
        return self


class QuizRead(BaseModel):
    id: int
    question_count: int
    questions: list[QuestionRead]

    model_config = {"from_attributes": True}


class AnswerUserRead(BaseModel):
    text: str
    model_config = {"from_attributes": True}


class QuestionUserRead(BaseModel):
    text: str
    type: AnswerType
    answers: list[AnswerUserRead]

    model_config = {"from_attributes": True}


class QuizUserRead(BaseModel):
    token: str
    question_count: int
    question: list[QuestionUserRead]
    model_config = {"from_attributes": True}


class QuizAnswers(BaseModel):
    answers: list[int]


class QuizSessionAnswer(BaseModel):
    status: str
    procent: int
