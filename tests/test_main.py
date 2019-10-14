import pytest
from pytest import fixture
from pro_lambda import pro_lambda, tools
import asyncio


def test_main():
    some = pro_lambda(lambda : 1)
    other = some + 1
    assert other() == 2

    some = pro_lambda(lambda x, y: x+y)
    other = some + 1
    assert other(1, 2) == 4

    other = some + (lambda z, y: z - y)
    assert other(1, y = 2, z = 3) == 4


@pytest.mark.asyncio
async def test_async():

    async def _some(x):
        await asyncio.sleep(0.3)
        return x

    _save = _some
    some = pro_lambda(_some)
    other = some + (lambda: 1)
    assert some.is_async
    assert await other(1) == 2

    some = pro_lambda(lambda : 1)
    other = some + _some

    assert other.is_async
    assert await other(x=1) == 2

    some = pro_lambda(_some)
    other = some + _some
    assert other.is_async
    assert await other(x=1) == 2

    other = some == 1

    assert other.is_logical
    assert await other(1)
    assert not await other(2)

    other = some + _some(2)

    assert other.is_logical
    assert await other(1) == 3

    some = pro_lambda(lambda : 1)
    other = some + _some(1)
    assert await other() == 2

    some = pro_lambda(lambda **kwargs: kwargs.get('x', 1))
    other = some + _some(1)
    assert await other() == 2


def test_tools():
    with pytest.raises(Exception):
        with tools.log_exception('some message'):
            raise Exception('hello')