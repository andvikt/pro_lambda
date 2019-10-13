import typing
import inspect
import functools
import logging
from contextlib import contextmanager
import asyncio
import abc

logger = logging.getLogger('pro_lambda')


class ClsInitMeta(abc.ABCMeta):
    """
    Special metaclass for making class initialisers with @cls_init decorator
    """

    def __new__(mcls, name, bases, namespace: dict, **kwargs):
        _inits = {}
        for x, y in namespace.items():
            if hasattr(y, '_is_cls_init'):
                _inits[x] = y
        for x in _inits:
            namespace.pop(x)

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        for x in _inits.values():
            x(cls)

        return cls


def cls_init(foo):
    """
    Decorator, mark foo as class initialisier
    """
    setattr(foo, '_is_cls_init', True)
    return foo


def _is_async(*foo):
    """
    Returns True if function is coroutinefunction or if it returns Awaitable
    Args:
        *foo:

    Returns:

    """
    for x in foo:
        if getattr(x, '_is_async', False) or asyncio.iscoroutinefunction(x):
            return True
    return False


def skip_not_needed_kwargs(foo):
    """
    Decorator, decorated foo will silently skip not needed kwargs
    """

    params: typing.Dict[str, inspect.Parameter] = inspect.signature(foo).parameters
    try:
        has_kwargs = max([x.kind is x.VAR_KEYWORD for x in params.values()])
    except ValueError:
        has_kwargs = False

    @functools.wraps(foo)
    def wrapper(*args, **kwargs):
        kwargs = {x: y for x, y in kwargs.items() if x in params}
        return foo(*args, **kwargs)

    if has_kwargs:
        return foo
    else:
        return wrapper


@contextmanager
def log_exception(msg: str = 'error in context', logger: logging.Logger = None, except_=None, raise_=True):
    """
    Contextmanager, while in this context, any exception will be logged with logger

    :param msg: msg for exception logger
    :param logger: logger to use with exceptions
    :param except_: iterable of exceptions to ignore in logging
    :param raise_: if False, will not raise exception, but will log it
    :return:
    """
    except_ = except_ or []
    logger = logger or logging.getLogger()
    _exc = []
    try:
        yield _exc
    except Exception as exc:
        _exc.append(exc)
        if exc.__class__ not in except_:
            logger.exception(msg)
        if raise_:
            raise


def deco_log_exception(msg, logger: logging.Logger=None, except_=None, raise_=True):
    """
    Decorator, decorated foo runs with exception logger

    Args:
        logger: logger to use, by default root is used
        except_: exceptions that should be ignored (not logged)
        raise_: if False, will not raise exception, only logs it
    """
    def deco(foo):

        @functools.wraps(foo)
        def wrapper(*args, **kwargs):
            with log_exception(msg, logger, except_=except_, raise_=raise_):
                return foo(*args, **kwargs)

        @functools.wraps(foo)
        async def async_wrapper(*args, **kwargs):
            with log_exception(msg, logger, except_=except_, raise_=raise_):
                return await foo(*args, **kwargs)

        if not asyncio.iscoroutinefunction(foo):
            return wrapper
        else:
            return async_wrapper

    return deco