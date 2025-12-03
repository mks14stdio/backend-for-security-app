import pytest


from src.scheme.article import ArticleRead

from .utils import create_article, create_module, create_module_item

from .conftest import client

from src.scheme.module import ModuleCreate, ModuleRead, ModuleUpdate




@pytest.mark.asyncio
async def test_create_module(client):

    async def make_article():
        article = create_article(content="My Hello World Content")
        result = await client.post("/v1/article/", json=article)
        assert result.status_code == 200
        return ArticleRead.model_validate(result.json()).id

    items = [create_module_item(title="Hello World", article_id=await make_article()) for i in range(3)]

    module = create_module(title="Hello World",items=items)
    result = await client.post("/v1/module/", json=module)

    assert result.status_code == 200
    result_body = ModuleRead.model_validate(result.json())
    assert result_body.title == "Hello World"
    assert result_body.items[0].title == "Hello World"
    assert len(result_body.items) == 3

@pytest.mark.asyncio
async def test_delete_module(client):
    async def make_article():
        article = create_article(content="My Hello World Content")
        result = await client.post("/v1/article/", json=article)
        assert result.status_code == 200
        return ArticleRead.model_validate(result.json()).id

    items = [create_module_item(title="Hello World", article_id=await make_article()) for i in range(3)]

    module = create_module(title="Hello World", items=items)
    result = await client.post("/v1/module/", json=module)

    assert result.status_code == 200
    module_read = ModuleRead.model_validate(result.json())
    assert module_read.title == "Hello World"
    assert len(module_read.items) == 3

    result = await client.delete(f"/v1/module/{module_read.id}")
    assert result.status_code == 200

    result = await client.get(f"/v1/module/{module_read.id}")
    assert result.status_code == 404


@pytest.mark.asyncio
async def test_delete_module_item(client):
    async def make_article():
        article = create_article(content="My Hello World Content")
        result = await client.post("/v1/article/", json=article)
        assert result.status_code == 200
        return ArticleRead.model_validate(result.json()).id

    items = [create_module_item(title="Hello World", article_id=await make_article()) for i in range(15)]

    module = create_module(title="Hello World", items=items)
    result = await client.post("/v1/module/", json=module)

    assert result.status_code == 200
    module_read = ModuleRead.model_validate(result.json())
    assert module_read.title == "Hello World"
    assert len(module_read.items) == 15

    result = await client.delete(f"/v1/module/{module_read.id}/item/{module_read.items[3].order_index}")
    assert result.status_code == 200

    result = await client.get(f"/v1/module/{module_read.id}")
    assert result.status_code == 200
    module_read = ModuleRead.model_validate(result.json())
    assert module_read.title == "Hello World"
    assert len(module_read.items) == 14

    for index, item in enumerate(module_read.items):
        assert item.order_index == index