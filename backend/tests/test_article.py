"""
Tests for Article API endpoints.

This module tests CRUD operations for articles, including:
- Creating articles with and without test associations
- Retrieving articles
- Updating article content and associations
- Deleting articles
"""

import pytest

from .utils import create_answer, create_article, create_question, create_test
from src.scheme.article import ArticleRead, ArticleUpdate
from src.scheme.test import QuestionType


# ============================================================================
# FIXTURES & HELPERS
# ============================================================================

SAMPLE_CONTENT = "My Hello World Content"
LARGE_CONTENT = "".join(["a" for _ in range(300000)])


async def create_test_with_question(client):
    """Helper: Create a test with a question and return test_id."""
    question = create_question(
        text="Is it true?",
        type=QuestionType.single,
        answers=[
            create_answer(text="Yes", is_correct=True),
            create_answer(text="No", is_correct=False),
        ],
    )
    test = create_test(title="Test 1", questions=[question])

    response = await client.post("/v1/test/", json=test)
    assert response.status_code == 200
    return response.json()["id"]


async def post_article(client, content: str, test_pk: int | None = None) -> ArticleRead:
    """Helper: Create an article via POST and return ArticleRead object."""
    article_data = create_article(content=content, test_pk=test_pk)
    response = await client.post("/v1/article/", json=article_data)
    assert response.status_code == 200
    return ArticleRead.model_validate(response.json())


# ============================================================================
# CREATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_create_article_without_test_association(client):
    """Test creating an article without a test association."""
    article = create_article(content=LARGE_CONTENT)
    result = await client.post("/v1/article/", json=article)

    assert result.status_code == 200
    result_body = ArticleRead.model_validate(result.json())
    assert result_body.content == LARGE_CONTENT
    assert result_body.test_pk is None


@pytest.mark.asyncio
async def test_create_article_with_test_association(client):
    """Test creating an article with a test_pk association."""
    test_id = await create_test_with_question(client)

    article = create_article(content=SAMPLE_CONTENT, test_pk=test_id)
    result = await client.post("/v1/article/", json=article)

    assert result.status_code == 200
    result_body = ArticleRead.model_validate(result.json())
    assert result_body.content == SAMPLE_CONTENT
    assert result_body.test_pk == test_id


# ============================================================================
# RETRIEVAL TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_get_article_by_id(client):
    """Test retrieving a single article by ID."""
    # Create article
    article_obj = await post_article(client, SAMPLE_CONTENT)

    # Retrieve it
    result = await client.get(f"/v1/article/{article_obj.id}")

    assert result.status_code == 200
    result_body = ArticleRead.model_validate(result.json())
    assert result_body.id == article_obj.id
    assert result_body.content == SAMPLE_CONTENT


@pytest.mark.asyncio
async def test_get_nonexistent_article(client):
    """Test retrieving a non-existent article returns 404."""
    result = await client.get("/v1/article/99999")
    assert result.status_code == 404


# ============================================================================
# UPDATE TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_update_article_content(client):
    """Test updating article content via PATCH."""
    article_obj = await post_article(client, SAMPLE_CONTENT)

    new_content = "My Hello World Content 2"
    update_data = create_article(content=new_content)
    result = await client.patch(f"/v1/article/{article_obj.id}", json=update_data)

    assert result.status_code == 200
    result_body = ArticleRead.model_validate(result.json())
    assert result_body.content == new_content
    assert result_body.id == article_obj.id


@pytest.mark.asyncio
async def test_add_test_association_to_article(client):
    """Test adding a test association to an existing article."""
    # Create article without test
    article_obj = await post_article(client, SAMPLE_CONTENT)
    assert article_obj.test_pk is None

    # Create a test
    test_id = await create_test_with_question(client)

    # Add test association via update
    update_data = create_article(content=SAMPLE_CONTENT, test_pk=test_id)
    result = await client.patch(f"/v1/article/{article_obj.id}", json=update_data)

    assert result.status_code == 200
    updated_article = ArticleRead.model_validate(result.json())
    assert updated_article.test_pk == test_id



@pytest.mark.asyncio
async def test_delete_article(client):
    """Test deleting an article via DELETE endpoint."""
    article_obj = await post_article(client, SAMPLE_CONTENT)

    # Delete it
    result = await client.delete(f"/v1/article/{article_obj.id}")
    assert result.status_code == 200

    # Verify it's gone
    result = await client.get(f"/v1/article/{article_obj.id}")
    assert result.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_article(client):
    result = await client.delete("/v1/article/99999")
    assert result.status_code in [400, 404]