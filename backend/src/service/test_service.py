from email.policy import HTTP
from math import e
from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import question
from src.models.test import Test
from src.service.question_service import QuestionService
from src.repository.test_repository import TestRepository

from src.scheme.test import (QuestionAnswerCreate, QuestionAnswerRead, QuestionBase, 
                             QuestionRead, QuestionCreate, QuestionUpdate, TestBase, 
                             TestCreate, TestRead)

class TestService:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.test_repo = TestRepository(session)
        self.question_service = QuestionService(session)

    
    async def add_test(self, test: TestCreate):
        try:
            test_dict = TestBase(title=test.title, questions_count=len(test.questions))
            test_db = await self.test_repo.add_one_test(test_dict.model_dump())
            await self.session.commit()

            questions = await self.question_service.add_all_question(test.questions, test_db.id)
            await self.session.refresh(test_db)

            result = TestRead(
                id=test_db.id, title=test_db.title, questions_count=test_db.questions_count, questions=questions
            )
            return result

        except Exception as e:
            await self.session.rollback()
            print(e)
            raise HTTPException(400, f"{e}")

    async def delete_test(self, test_id: int):
        try:
            if test_id:
                await self.test_repo.delete_one_test(test_id)
                await self.session.commit()
                return {"message": "Test deleted successfully"}
        except Exception as e:
                print(e)
                raise HTTPException(400, "Test id is required")
        
    
    async def find_one(self, test_id: int):
        try:
            test: Test = await self.test_repo.find_one(test_id)
            return TestRead.model_validate(test)
        except Exception as e:
            raise HTTPException(404, f"Тест не найден")
        
    async def add_question(self, test_id: int, question: QuestionCreate):
        try:
            new_question = await self.question_service.add_one_question(question, test_id)
            return new_question
        except Exception as e:
            print(e)
            raise HTTPException(400, f"Что-то случилось я хз лол {e}")