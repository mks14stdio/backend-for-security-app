import pytest

from .conftest import get_db

from src.scheme.auth import RegisterScheme

@pytest.mark.anyio
async def test_register_user(get_db):

    user = create_user(name="Denis Sova", password="qweasd123", email="dsova@sfedu.ru")
    assert 1 == 1

    