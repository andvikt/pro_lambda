import asyncio
from pro_lambda import pro_lambda


async def main():

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

asyncio.run(main())
