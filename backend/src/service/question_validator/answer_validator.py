from abc import ABC, abstractmethod
from asyncio import QueueEmpty
from typing import Any, List
from src.scheme.test import QuestionCreate
from src.models.question import QuestionType

class AnswerValidator(ABC):
    type: Any 

    def validate_creation_question(self, question: QuestionCreate) -> bool:
        raise NotImplemented
    

class SingleValidator(AnswerValidator):
    type: QuestionType = QuestionType.single

    def validate_creation_question(self, question: QuestionCreate) -> bool:
        validate = [1 for i in question.answers if i.is_correct == True]
        return len(validate) == 1
    
class MultipleAndTextValidator(AnswerValidator):
    type: List[QuestionType] = [QuestionType.multiple, QuestionType.text]

    def validate_creation_question(self, question: QuestionCreate) -> bool:
        validate = [1 for i in question.answers if i.is_correct == True]
        return len(validate) > 1
    

a = MultipleAndTextValidator()
b = SingleValidator()

class FactoryAnswerValidator:
    @staticmethod
    def create(type: QuestionType):
        match type:
            case QuestionType.multiple:
                return a
            case QuestionType.text:
                return a
            case QuestionType.single:
                return b