from venv import create
import pytest

from src.models.question import QuestionType
from src.scheme.test import TestCreate, TestRead
from src.scheme.article import ArticleCreate, ArticleRead, ArticleUpdate

from .utils import create_article, create_question, create_test, create_answer

@pytest.mark.asyncio
async def test_create_user(client):
    test = create_test(title="Test 1", questions=[
        create_question(text="Is it true?", type=QuestionType.single, answers=[
            create_answer(text="Yes", is_correct=True),
            create_answer(text="No", is_correct=False)
        ]),
        create_question(text="Is it false?", type=QuestionType.single, answers=[
            create_answer(text="Yes", is_correct=False),
            create_answer(text="No", is_correct=True)
        ])
    ])

    result = await client.post("/v1/test/", json=test)
    assert result.status_code == 200
    result_body = TestRead.model_validate(result.json())
    assert result_body.title == "Test 1"
    assert result_body.questions_count == 2
    assert len(result_body.questions) == 2
    assert result_body.questions[0].type == QuestionType.single
    assert result_body.questions[1].type == QuestionType.single


