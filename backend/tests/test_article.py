from turtle import update
import pytest

from .utils import create_answer, create_article, create_question, create_test

from .conftest import get_db

from src.scheme.article import ArticleBase, ArticleCreate, ArticleRead, ArticleUpdate
from src.scheme.test import TestCreate, TestRead, QuestionCreate, QuestionAnswerCreate, QuestionType

from src.api.dependecy import SecurityDep

@pytest.mark.asyncio
async def test_create_without_test_pk(client):
    
    article_text = "".join(['a' for i in range(300000)])

    article = create_article(content=article_text)
    result = await client.post("/v1/article/", json=article)

    assert result.status_code == 200    
    result_body = ArticleRead.model_validate(result.json())
    assert result_body.content == article_text

@pytest.mark.asyncio
async def test_create_with_test_pk(client):

    question = create_question(text="Is it true?", type=QuestionType.single, answers=[
        create_answer(text="Yes", is_correct=True),
        create_answer(text="No", is_correct=False)
    ])

    test = create_test(title="Test 1", questions=[question])

    result = await client.post("/v1/test/", json=test)
    assert result.status_code == 200
    result_body = result.json() 
    test_id = result_body["id"] 
    
    article = create_article(content="My Hello World Content", test_pk=test_id)
    
    result = await client.post("/v1/article/", json=article)
    assert result.status_code == 200
    result_body = result.json()
    
    assert result_body["content"] == "My Hello World Content"
    assert result_body["test_pk"] == test_id 

@pytest.mark.asyncio
async def test_change_article(client):
    article = create_article(content="My Hello World Content")
    result = await client.post("/v1/article/", json=article)
    assert result.status_code == 200
    result_body = ArticleRead.model_validate(result.json())
    assert result_body.content == "My Hello World Content"

    article = create_article(content="My Hello World Content 2")
    print(result_body.id)
    result = await client.patch(f"/v1/article/{result_body.id}", json=article)

    assert result.status_code == 200
    result_body = ArticleRead.model_validate(result.json())
    assert result_body.content == "My Hello World Content 2"

@pytest.mark.asyncio
async def test_get_article(client):
    article = create_article(content="My Hello World Content")
    result = await client.post("/v1/article/", json=article)
    assert result.status_code == 200
    result_body = ArticleRead.model_validate(result.json())
    assert result_body.content == "My Hello World Content"

    result = await client.get(f"/v1/article/{result_body.id}")

    assert result.status_code == 200
    result_body = ArticleRead.model_validate(result.json())
    assert result_body.content == "My Hello World Content"

@pytest.mark.asyncio
async def test_add_article_to_test(client):
    question = create_question(text="Is it true?", type=QuestionType.single, answers=[
        create_answer(text="Yes", is_correct=True),
        create_answer(text="No", is_correct=False)
    ])

    test = create_test(title="Test 1", questions=[question])

    result = await client.post("/v1/test/", json=test)
    assert result.status_code == 200
    result_body = result.json() 
    test_id = result_body["id"] 

    article = create_article(content="My Hello World Content")
    
    result = await client.post("/v1/article/", json=article)
    assert result.status_code == 200
    result_body = result.json()
    
    article_read = ArticleRead.model_validate(result_body)
    assert article_read.content == "My Hello World Content"
    assert article_read.test_pk == None

    article = create_article(content="My Hello World Content", test_pk=test_id)
    result = await client.patch(f"/v1/article/{article_read.id}", json=article)

    update_article = ArticleRead.model_validate(result.json())
    assert update_article.test_pk == test_id

@pytest.mark.asyncio
async def test_delete_article(client):
    article = create_article(content="My Hello World Content")
    result = await client.post("/v1/article/", json=article)
    assert result.status_code == 200
    result_body = ArticleRead.model_validate(result.json())
    assert result_body.content == "My Hello World Content"

    result = await client.delete(f"/v1/article/{result_body.id}")
    assert result.status_code == 200

    result = await client.get(f"/v1/article/{result_body.id}")
    assert result.status_code == 404