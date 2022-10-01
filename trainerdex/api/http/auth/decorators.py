from functools import wraps
from typing import Callable, Iterable, ParamSpec, Type, TypeVar

from trainerdex.api.exceptions import Forbidden
from trainerdex.api.http.base import BaseHTTPClient

P = ParamSpec("P")
T = TypeVar("T")


def requires_authentication(
    func: Callable[P, T] = None, authenticators: Iterable[Type[BaseHTTPClient]] = []
) -> Callable[P, T]:
    """Decorator for methods that require authentication."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(self: BaseHTTPClient, *args, **kwargs) -> T:
            if authenticators and not isinstance(self, tuple(authenticators)):
                raise TypeError(
                    f"Method {func.__name__} only supports the following Authenticators: {', '.join(authenticator.__name__ for authenticator in authenticators)}"
                )

            if not self.authenticated:
                raise Forbidden(f"Method {func.__name__} requires authentication.")
            return func(self, *args, **kwargs)

        return wrapper

    if func:
        return decorator(func)
    else:
        return decorator
