import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.article import Article
from src.models.module import Module
from tests.conftest import URL_PREFIX
from tests.factory import create_article, create_module

MODULE_URL_PREFIX = URL_PREFIX + "/admin/modules"
USER_MODULE_URL_PREFIX = URL_PREFIX + "/modules"
ARTICLE_URL_PREFIX = URL_PREFIX + "/articles"


@pytest.mark.asyncio
async def test_create_module(auth_client: AsyncClient, db_session: AsyncSession):
    articles: list[Article] = [await create_article(db_session) for i in range(5)]

    payload = {
        "title": "Hello World",
        "description": "HI",
        "items": [{"article_id": article.id} for article in articles],
    }

    response = await auth_client.post(f"{MODULE_URL_PREFIX}/", json=payload)

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "Hello World", data
    assert data["description"] == "HI", data
    assert len(data["items"]) == 5, data


@pytest.mark.asyncio
async def test_change_module(auth_client: AsyncClient, db_session: AsyncSession):
    articles: list[Article] = [await create_article(db_session) for i in range(3)]
    module: Module = await create_module(db_session)

    payload = {
        "title": "Changed title",
        "items": [{"article_id": article.id} for article in articles],
    }

    response = await auth_client.patch(f"{MODULE_URL_PREFIX}/{module.id}", json=payload)

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Changed title", data
    assert not data["description"], data
    assert len(data["items"]) == 3, data


@pytest.mark.asyncio
async def test_read_modules_info(auth_client: AsyncClient, db_session: AsyncSession):
    articles: list[Article] = [await create_article(db_session) for i in range(15)]
    modules: list[Module] = [
        await create_module(
            db_session, items=articles, description="This is description"
        )
        for i in range(5)
    ]

    response = await auth_client.get(f"{USER_MODULE_URL_PREFIX}/")

    assert response.status_code == 200, response.text
    data = response.json()

    assert data.get("modules", None), response.text
    responce_data = data["modules"]

    assert len(modules) == 5, response.text
    assert responce_data[0]["description"] == "This is description", response.text
    assert responce_data[0]["total"] == 15, response.text
    assert responce_data[0]["completed"] == 0, response.text


@pytest.mark.asyncio
async def test_modules_info_after_read_article(
    auth_client: AsyncClient, db_session: AsyncSession
):
    articles: list[Article] = [await create_article(db_session) for i in range(15)]
    modules: list[Module] = [
        await create_module(
            db_session, items=articles, description="This is description"
        )
        for i in range(5)
    ]

    response = await auth_client.post(f"v1/articles/{articles[1].id}/read")

    assert response.status_code == 202, response.text

    response = await auth_client.get(f"{USER_MODULE_URL_PREFIX}/")

    assert response.status_code == 200, response.text
    data = response.json()

    assert data.get("modules", None), response.text
    responce_data = data["modules"]

    assert len(modules) == 5, response.text
    assert responce_data[0]["description"] == "This is description", response.text
    assert responce_data[0]["total"] == 15, response.text
    assert responce_data[0]["completed"] == 1, response.text
