import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio
async def test_create_article(auth_client: AsyncClient):
    payload = {
        "title": "Test article",
        "content": "hello",
    }

    response = await auth_client.post("v1/articles/", json=payload)

    assert response.status_code == 201, response.text
    data = response.json()

    assert data["title"] == "Test article", response.text


@pytest.mark.asyncio
async def test_delete_article(auth_client: AsyncClient, db_session: AsyncSession):
    from src.models.article import Article
    from tests.factory import create_article

    article: Article = await create_article(db_session)

    response = await auth_client.delete(f"v1/articles/{article.id}")

    assert response.status_code == 204, response.text

    response_after = await auth_client.delete(f"v1/articles/{article.id}")

    assert response_after.status_code == 404, response.text


@pytest.mark.asyncio
async def test_change_content_article(
    auth_client: AsyncClient, db_session: AsyncSession
):
    from src.models.article import Article
    from tests.factory import create_article

    payload = {"title": "New Title", "content": "New Content"}

    article: Article = await create_article(db_session)

    response = await auth_client.patch(f"v1/articles/{article.id}", json=payload)

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
        {"answer": "True", "is_correct": True},
        {"answer": "False", "is_correct": False},
    ]

    questions_template = [
        {"question": "Is Read?", "type": "single", "answers": answers_template}
        for _ in range(10)
    ]

    payload = {
        "count_questions": 5,
        "questions": questions_template,
    }

    response = await auth_client.put(f"v1/articles/{article.id}/test", json=payload)

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["count_questions"] == 5, response.text
    assert len(data["questions"]) == 10, response.text
