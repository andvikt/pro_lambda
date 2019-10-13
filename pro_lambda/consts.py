import operator as op
import typing

T = typing.TypeVar('T')

ops = [
    ('__add__', op.__add__),
    ('__sub__', op.__sub__),
    ('__mul__', op.__mul__),
    ('__truediv__', op.__truediv__),
    ('__floordiv__', op.__floordiv__),
    ('__mod__', op.__mod__),
    ('__pow__', op.__pow__),
    ('__lt__', op.__lt__),
    ('__gt__', op.__gt__),
    ('__le__', op.__le__),
    ('__ge__', op.__ge__),
    ('__eq__', op.__eq__),
    ('__ne__', op.__ne__),
    ('__and__', op.__and__),
    ('__or__', op.__or__),
    ('__invert__', op.__not__),
]

logical = [
    '__lt__',
    '__gt__',
    '__le__',
    '__ge__',
    '__eq__',
    '__ne__',
    '__and__',
    '__or__',
    '__invert__',
]