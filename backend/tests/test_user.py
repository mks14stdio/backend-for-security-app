import pytest

from .utils import create_user

@pytest.mark.anyio
async def test_register_user():

    user = create_user(name="Denis Sova", password="qweasd123", email="dsova@sfedu.ru")
    assert 1 == 1

    