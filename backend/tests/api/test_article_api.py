import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from tests.conftest import URL_PREFIX

ARTICLE_URL_PREFIX = URL_PREFIX + "/admin/articles"
USER_ARTICLE_URL_PREFIX = URL_PREFIX + "/articles"


@pytest.mark.asyncio
async def test_create_article(auth_client: AsyncClient):
    payload = {
        "title": "Test article",
        "content": "hello",
    }

    response = await auth_client.post(f"{ARTICLE_URL_PREFIX}/", json=payload)

    assert response.status_code == 201, response.text
    data = response.json()

    assert data["title"] == "Test article", response.text


@pytest.mark.asyncio
async def test_delete_article(auth_client: AsyncClient, db_session: AsyncSession):
    from src.models.article import Article
    from tests.factory import create_article

    article: Article = await create_article(db_session)

    response = await auth_client.delete(f"{ARTICLE_URL_PREFIX}/{article.id}")

    assert response.status_code == 204, response.text

    response_after = await auth_client.delete(f"{ARTICLE_URL_PREFIX}/{article.id}")

    assert response_after.status_code == 404, response.text


@pytest.mark.asyncio
async def test_change_content_article(
    auth_client: AsyncClient, db_session: AsyncSession
):
    from src.models.article import Article
    from tests.factory import create_article

    payload = {"title": "New Title", "content": "New Content"}

    article: Article = await create_article(db_session)

    response = await auth_client.patch(
        f"{ARTICLE_URL_PREFIX}/{article.id}", json=payload
    )

    assert response.status_code == 200, response.text
    data = response.json()

    assert data["title"] == "New Title", response.text
    assert data["content"] == "New Content", response.text


@pytest.mark.asyncio
async def test_add_article_quiz(auth_client: AsyncClient, db_session: AsyncSession):
    from src.models.article import Article
    from tests.factory import create_article

    article: Article = await create_article(db_session)

    answers_template = [
        {"text": "True", "is_correct": True},
        {"text": "False", "is_correct": False},
    ]

    questions_template = [
        {"text": "Is Read?", "type": "single", "answers": answers_template}
        for _ in range(10)
    ]

    payload = {
        "question_count": 5,
        "questions": questions_template,
    }

    response = await auth_client.put(
        f"{ARTICLE_URL_PREFIX}/{article.id}/test", json=payload
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["question_count"] == 5, response.text
    assert len(data["questions"]) == 10, response.text


@pytest.mark.asyncio
async def test_change_article_quiz(auth_client: AsyncClient, db_session: AsyncSession):
    from src.models.article import Article
    from tests.factory import create_article, create_quiz

    article: Article = await create_article(db_session)
    await create_quiz(db_session, article)

    answers_template = [
        {"text": "True", "is_correct": True},
        {"text": "False", "is_correct": False},
    ]

    questions_template = [
        {"text": "Is Read?", "type": "single", "answers": answers_template}
        for _ in range(30)
    ]

    payload = {
        "question_count": 10,
        "questions": questions_template,
    }

    response = await auth_client.put(
        f"{ARTICLE_URL_PREFIX}/{article.id}/test", json=payload
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["question_count"] == 10, response.text
    assert len(data["questions"]) == 30, response.text


@pytest.mark.asyncio
async def test_read_article_with_quiz(
    auth_client: AsyncClient, db_session: AsyncSession
):
    from src.models.article import Article
    from tests.factory import create_article, create_quiz

    article: Article = await create_article(db_session)
    await create_quiz(db_session, article)

    response = await auth_client.post(f"{USER_ARTICLE_URL_PREFIX}/{article.id}/read")

    assert response.status_code == 409, response.text


@pytest.mark.asyncio
async def test_quiz_count_negative(auth_client: AsyncClient, db_session: AsyncSession):
    from src.models.article import Article
    from tests.factory import create_article

    article: Article = await create_article(db_session)

    answers_template = [
        {"text": "True", "is_correct": True},
        {"text": "False", "is_correct": False},
    ]

    questions_template = [
        {"text": "Is Read?", "type": "single", "answers": answers_template}
        for _ in range(10)
    ]

    payload = {
        "question_count": -1,
        "questions": questions_template,
    }

    response = await auth_client.put(
        f"{ARTICLE_URL_PREFIX}/{article.id}/test", json=payload
    )

    assert response.status_code == 422, response.text


@pytest.mark.asyncio
async def test_quiz_count_greater(auth_client: AsyncClient, db_session: AsyncSession):
    from src.models.article import Article
    from tests.factory import create_article

    article: Article = await create_article(db_session)

    answers_template = [
        {"text": "True", "is_correct": True},
        {"text": "False", "is_correct": False},
    ]

    questions_template = [
        {"text": "Is Read?", "type": "single", "answers": answers_template}
        for _ in range(10)
    ]

    payload = {
        "question_count": 30,
        "questions": questions_template,
    }

    response = await auth_client.put(
        f"{ARTICLE_URL_PREFIX}/{article.id}/test", json=payload
    )

    assert response.status_code == 422, response.text


@pytest.mark.asyncio
async def test_quiz_question_dont_have_correct_answer(
    auth_client: AsyncClient, db_session: AsyncSession
):
    from src.models.article import Article
    from tests.factory import create_article

    article: Article = await create_article(db_session)

    answers_template = [
        {"text": "True", "is_correct": False},
        {"text": "False", "is_correct": False},
    ]

    questions_template = [
        {"text": "Is Read?", "type": "single", "answers": answers_template}
        for _ in range(10)
    ]

    payload = {
        "question_count": 5,
        "questions": questions_template,
    }

    response = await auth_client.put(
        f"{ARTICLE_URL_PREFIX}/{article.id}/test", json=payload
    )

    assert response.status_code == 422, response.text


@pytest.mark.asyncio
async def test_quiz_question_type_signle_fail(
    auth_client: AsyncClient, db_session: AsyncSession
):
    from src.models.article import Article
    from tests.factory import create_article

    article: Article = await create_article(db_session)

    answers_template = [
        {"text": "True", "is_correct": True},
        {"text": "False", "is_correct": True},
    ]

    questions_template = [
        {"text": "Is Read?", "type": "single", "answers": answers_template}
        for _ in range(10)
    ]

    payload = {
        "question_count": 5,
        "questions": questions_template,
    }

    response = await auth_client.put(
        f"{ARTICLE_URL_PREFIX}/{article.id}/test", json=payload
    )

    assert response.status_code == 422, response.text
