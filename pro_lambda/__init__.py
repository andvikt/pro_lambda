import asyncio
import functools
from copy import copy
import typing
import abc
from . import tools, consts
import inspect


class pro_lambda(metaclass=tools.ClsInitMeta):
    """
    Модификатор функций, который наделяет функцию арифметическими способностями.
    Например, если исходная функция выглядит так:

    >>> some = pro_lambda(lambda : 1)

    Теперь some можно использовать с любыми математическими операциями:

    >>> other = some + 1
    >>> other() # 1 + 1
    2

    А так же с другими функциями:
    >>> other = other - lambda: 10
    >>> other() # 1 + 1 - 10
    8

    Или другими LambdaMaths (LambdaMath по сути тоже функция, т.к. определяет метод __call__:

    >>> other = other + pro_lambda(lambda : 8)
    >>> other()
    0

    Кроме того, исходная функция может быть и сложной (содержать параметры):
    >>> some = pro_lambda(lambda x, y: x + y)
    >>> other = some - 5
    >>> other(1, 1) # 1 + 1 - 5
    3

    И так же можно комбинировать с другими функциями с параметрами, параметры правой функции при этом станут keyword-only
    параметрами итоговой функции:

    >>> some = pro_lambda(lambda x, y: x + y)
    >>> other = some + lambda z, y: z - y
    >>> other(1, 2, z=3) # (1 + 2) - (3 - 2)
    2

    Кроме того, если любой из участников вычисления является асинхронной функцией или awaitable-объектом, то конечная
    функция так же становится асинхронной:

    >>> async def foo():
    ...     await asyncio.sleep(1)
    ...     return 1
    >>> some = pro_lambda(foo)
    >>> other = some + 1
    >>> await other()
    2

    Поддерживаемые операторы: + - / * **
    Так же поддерживаются логические операторы: > >= < <= & | ==

    """

    def __init__(self, foo: typing.Callable):
        self.foo = tools.skip_not_needed_kwargs(foo)
        self._is_async = asyncio.iscoroutinefunction(foo)
        self._is_logical = False

    def __call__(self, *args, **kwargs) -> typing.Awaitable:
        return self.foo(*args, **kwargs)

    @property
    def is_async(self):
        """
        If self.foo is async foo or it returns awaitable returns True
        """
        return self._is_async

    @property
    def is_logical(self):
        """
        Returns True if self.foo is a product of logical operator (==, >, >=, <, <=, &, |)
        """
        return self._is_async

    @tools.cls_init
    def _add_maths(cls):

        def set_foo(params):
            name, op = params

            def wrapper(self: 'pro_lambda', other=None):
                ret = copy(self)
                _other = other

                setattr(ret, '_is_async', tools._is_async(other, self))
                if isinstance(other, typing.Callable):
                    other = tools.skip_not_needed_kwargs(other)

                def _foo_simple(*args, **kwargs):
                    return op(self(*args, **kwargs), other)

                def _other_callable(*args, **kwargs):
                    return op(self(*args, **kwargs), other(**kwargs))

                async def _self_async(*args, **kwargs):
                    return op(await self(*args, **kwargs), other)

                async def _other_async(*args, **kwargs):
                    return op(self(*args, **kwargs), await other(**kwargs))

                async def _both_async(*args, **kwargs):
                    return op(await self(*args, **kwargs), await other(**kwargs))

                async def _self_async_other_awaitable(*args, **kwargs):
                    return op(await self(*args, **kwargs), await other)

                async def _self_async_other_callable(*args, **kwargs):
                    return op(await self(*args, **kwargs), other(**kwargs))

                async def _other_awaitable(*args, **kwargs):
                    return op(self(*args, **kwargs), await other)

                if not self.is_async:
                    if isinstance(_other, typing.Awaitable):
                        ret.foo = _other_awaitable
                    elif tools._is_async(_other):
                        ret.foo = _other_async
                    elif isinstance(_other, typing.Callable):
                        ret.foo = _other_callable
                    else:
                        ret.foo = _foo_simple
                else:
                    if isinstance(_other, typing.Awaitable):
                        ret.foo = _self_async_other_awaitable
                    elif tools._is_async(_other):
                        ret.foo = _both_async
                    elif isinstance(_other, typing.Callable):
                        ret.foo = _self_async_other_callable
                    else:
                        ret.foo = _self_async

                setattr(ret, '_is_logical', name in consts.logical)
                #ret.foo = functools.wraps(self.foo)(ret.foo)  # TODO: do we really need this?
                ret.foo = tools.deco_log_exception(f'in {self}.{name}({other})', tools.logger)(ret.foo)
                return ret

            setattr(cls, name, wrapper)

        list(map(set_foo, consts.ops))

    def _inject_typing(self, other: consts.T = None) -> 'pro_lambda':
        """
        Just a convinience for IDE type-hinting
        """
        pass

    __add__ = _inject_typing
    __sub__ = _inject_typing
    __mul__ = _inject_typing
    __truediv__ = _inject_typing
    __floordiv__ = _inject_typing
    __mod__ = _inject_typing
    __pow__ = _inject_typing
    __lt__ = _inject_typing
    __gt__ = _inject_typing
    __le__ = _inject_typing
    __ge__ = _inject_typing
    __eq__ = _inject_typing
    __ne__ = _inject_typing
    __and__ = _inject_typing
    __or__ = _inject_typing
    __invert__ = _inject_typing
