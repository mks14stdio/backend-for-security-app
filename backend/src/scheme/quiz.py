import enum

from pydantic import BaseModel


class AnswerType(enum.Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"
    SELECTABLE = "selectable"


class AnswerCreate(BaseModel):
    answer: str
    is_correct: bool


class AnswerRead(BaseModel):
    answer: str


class QuestionCreate(BaseModel):
    question: str
    type: AnswerType
    answers: list[AnswerCreate]


class QuestionRead(BaseModel):
    question: str
    type: AnswerType
    answers: list[AnswerRead]


class QuizCreate(BaseModel):
    count_questions: int
    questions: list[QuestionCreate]


class QuizRead(BaseModel):
    token: str
    count_qustions: int
    questions: list[QuestionRead]
