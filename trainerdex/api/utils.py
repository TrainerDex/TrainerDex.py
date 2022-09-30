from inspect import isawaitable
from typing import Any, Callable, ParamSpec, TypeVar, Union, overload

from typing_extensions import Protocol, runtime_checkable

P = ParamSpec("P")
T = TypeVar("T")


@overload
def convert(cls: Callable[P, T]) -> Callable[P, T]:
    ...


@overload
def convert(cls: Callable[P, T], *args, **kwargs) -> Union[T, None]:
    ...


def convert(cls, *args, **kwargs):
    """This is very hacky!

    Generates a converter function
    Returns the function if no addictional args or kwargs are supplied, else runs the function
    """

    def convert(*args, **kwargs) -> Union[Any, None]:
        """This is very hacky!

        Special converter function generated by :method:`trainerdex.api.utils.convert`

        Attempts to return the output of a function, returns None if any exception occurs.

        ONLY USE THIS IF YOU KNOW WHAT YOU'RE DOING
        """
        try:
            return cls(*args, **kwargs)
        except Exception:
            return None

    if args or kwargs:
        return convert(*args, **kwargs)
    else:
        return convert


async def maybe_coroutine(f, *args, **kwargs):
    value = f(*args, **kwargs)
    if isawaitable(value):
        return await value
    else:
        return value


@runtime_checkable
class HasID(Protocol):
    id: int
