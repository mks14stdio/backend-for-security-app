from datetime import timedelta
from typing import List

from fastapi import HTTPException
from jwt import ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from src.models import Question
from src.models.token import TestSessionToken, TestSessionItem
from src.models.question import Question, QuestionAnswer
from src.repository.test_repository import TestRepository
from src.repository.question_answer_repository import QuestionAnswerRepository
from src.repository.question_repository import QuestionRepositroy
from src.repository.test_session_repositroy import TestSessionRepository

from src.scheme.session_user_testing import (
    SessionQuestionAnswerRead,
    SessionQuestionRead,
    SessionTestRead,
    SessionTestReponse,
    SessionQuestionRepsone,
)

from src.security import create_token, TokenType, decode_token


class SessionTestService:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.test_repository = TestRepository(session)
        self.test_session_repository = TestSessionRepository(session)
        self.question_repository = QuestionRepositroy(session)
        self.question_answer_repository = QuestionAnswerRepository(session)

    async def start(self, test_id: int) -> SessionTestReponse:

        try:
            test = await self.test_repository.find_one(test_id)
            if not test:
                raise HTTPException(status_code=404, detail="Тест не найден")

            questions = await self.question_repository.find_by_pk_test_random(
                pk_id=test_id,
                limit=test.questions_count,
            )

            if not questions:
                raise HTTPException(
                    status_code=400,
                    detail="Вопросы для теста не найдены",
                )

            payload = {
                "test_id": test_id,
                "questions_count": test.questions_count,
            }

            token = create_token(
                payload=payload,
                expires=timedelta(minutes=1 * test.questions_count),
                token_type=TokenType.SESSION_TEST_TOKEN,
            )

            session_token = await self.test_session_repository.add_one(token)

            for question in questions:
                await self.test_session_repository.add_item(test_session_pk=test_id, question_pk=question.id)

            await self.session.commit()

            session_questions = []
            for question in questions:
                answer_reads = [
                    SessionQuestionAnswerRead(id=answer.id, text=answer.text)
                    for answer in question.answers
                ]
                session_question = SessionQuestionRead(
                    id=question.id,
                    answer=answer_reads,
                )
                session_questions.append(session_question)

            question_responses = [
                SessionQuestionRepsone(
                    question_id=q.id,
                    answers=[a.id for a in q.answers],
                )
                for q in questions
            ]

            return SessionTestReponse(token=token, questions=question_responses)

        except HTTPException:
            raise
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при запуске сессии теста: {str(e)}",
            )

    async def respone(self, answers: SessionTestReponse):
        
        user_test_repositroy = await self.test_session_repository.find_one_by_token(answers.token)
        if not user_test_repositroy:
            raise HTTPException(status_code=404, detail="Токен не действителен")

        try:
            decode_token(answers.token)
        except ExpiredSignatureError as e:
            await self.test_session_repository.delete_one(answers.token)
            raise HTTPException(status_code=404, detail="Токен не действителен")

        questions_by_user = answers.questions

        