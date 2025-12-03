from typing import List
from unittest.mock import Base
from pydantic import BaseModel, ConfigDict


from src.models.question import QuestionType

class QuestionAnswerBase(BaseModel):
    text: str
    is_correct: bool
    question_pk: int
    

class QuestionAnswerCreate(BaseModel):
    text: str
    is_correct: bool

class QuestionAnswerRead(QuestionAnswerBase):
    id: int
    text: str

    model_config = ConfigDict(from_attributes=True)

class QuestionAnswerUpdate(BaseModel):
    text: str | None = None
    is_correct: bool | None = None

class QuestionBase(BaseModel):
    text: str
    type: QuestionType
    test_pk: int

class QuestionCreate(BaseModel):
    text: str
    type: QuestionType
    answers: List[QuestionAnswerCreate]

class QuestionReadForTest(QuestionBase):
    id: int
    answers: List[QuestionAnswerRead] | None = None

    model_config = ConfigDict(from_attributes=True)


class QuestionRead(QuestionBase):
    id: int
    answers: List[QuestionAnswerRead] | None = None

    model_config = ConfigDict(from_attributes=True)

class QuestionUpdate(BaseModel):
    type: QuestionType | None = None
    answer: List[QuestionAnswerUpdate] | None = None


class TestBase(BaseModel):
    title: str
    questions_count: int

class TestCreate(BaseModel):
    title: str
    questions: List[QuestionCreate]


class TestRead(BaseModel):
    id: int
    title: str
    questions_count: int
    questions: List[QuestionRead]
