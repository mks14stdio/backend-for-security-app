from abc import ABC, abstractmethod
from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from src.repository.question_answer_repository import QuestionAnswerRepository
from src.repository.question_repository import QuestionRepositroy
from src.scheme.test import QuestionAnswerBase, QuestionAnswerCreate, QuestionAnswerRead, QuestionBase, QuestionRead, QuestionCreate, QuestionUpdate
from src.models.question import QuestionType, Question

from .question_validator.answer_validator import FactoryAnswerValidator

    

class QuestionService:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = QuestionRepositroy(session)
        self.answer_repo = QuestionAnswerRepository(session)

    async def add_one_question(self, question: QuestionCreate, test_pk: int):
        
        result = FactoryAnswerValidator.create(question.type).validate_creation_question(question)
        if not result:
            raise HTTPException(400, f"Тип имеет {question.type}")
        
        try:
            question_base = QuestionBase(text=question.text, type=question.type, test_pk=test_pk)
            question_db = await self.repository.add_one_question(question_base.model_dump())

            answers = [QuestionAnswerBase(text=i.text, is_correct=i.is_correct, question_pk=question_db.id).model_dump() for i in question.answers]

            await self.answer_repo.add_all(answers)

            await self.session.commit()
            await self.session.refresh(question_db)
            return QuestionRead.model_validate(question_db)
        except Exception as e:
            await self.session.rollback()
            print(e)
            raise HTTPException(400)
        
    async def add_all_question(self, questions: List[QuestionCreate], test_pk: int):
        for m, i in enumerate(questions):
            if not FactoryAnswerValidator.create(i.type).validate_creation_question(i):
                raise HTTPException(400, f"Вопрос {m}: Тип имеет {i.type}")


        try:
            questions_db = []
            for i in questions:
                questions_base = QuestionBase(text=i.text, type=i.type, test_pk=test_pk).model_dump()
                question_db = await self.repository.add_one_question(questions_base)
                answers = [QuestionAnswerBase(text=j.text, is_correct=j.is_correct, question_pk=question_db.id).model_dump() for j in i.answers]

                await self.answer_repo.add_all(answers)
                await self.session.refresh(question_db)
                questions_db.append(question_db)

            
            await self.session.commit()


            return [
                QuestionRead.model_validate(q_db) for q_db in questions_db
            ]


        except Exception as e:
            await self.session.rollback()
            print(e)
            raise HTTPException(400)
        


