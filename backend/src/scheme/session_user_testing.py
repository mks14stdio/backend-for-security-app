

from typing import List
from unittest.mock import Base
from pydantic import BaseModel

from src.models import question

class SessionQuestionAnswerRead(BaseModel):
    id: int
    text: str

class SessionQuestionRead(BaseModel):
    id: int
    answer: List[SessionQuestionAnswerRead]

class SessionTestRead(BaseModel):
    id: int
    title: str
    question_count: int
    questions: List[SessionQuestionRead]

class SessionQuestionRepsone(BaseModel):
    question_id: int
    answers: List[int]

class SessionTestReponse(BaseModel):
    token: str
    questions: List[SessionQuestionRepsone]