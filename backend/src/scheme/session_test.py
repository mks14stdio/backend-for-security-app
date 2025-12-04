

from typing import List
from pydantic import BaseModel

from src.models import question

class SessionQuestionAnswerRead:
    id: int
    text: str

class SessionQuestionRead:
    id: int
    answer: List[SessionQuestionAnswerRead]

class SessionTestRead(BaseModel):
    id: int
    title: str
    question_count: int
    questions: List[SessionQuestionRead]


class SessionTestReponse(BaseModel):
    token: str
    