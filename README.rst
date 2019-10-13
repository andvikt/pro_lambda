Install
-------

.. code-block::bash

    pip3 install pro_lambda

Documentation
-------------

You can find documentation `here<http://www.readthedocs.org/projects/pro_lambda>`_.


Description
-----------

pro_lambda make it possible to modify your functions with standart mathematical and logical operators:

.. code-block::python

    from pro_lambda import pro_lambda

    some = pro_lambda(lambda : 1)
    other = some + 1
    # then we call result as if it was (lambda: 1)() + 1
    assert other() == 2

    some = pro_lambda(lambda x, y: x+y)
    other = some + 1
    # here we pass some arguments
    assert other(1, 2) == 4

    # we can also use another function on the right side
    other = some + (lambda z, y: z - y)
    assert other(1, y = 2, z = 3) == 4

It also supports async functions:

.. code-block::python

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
