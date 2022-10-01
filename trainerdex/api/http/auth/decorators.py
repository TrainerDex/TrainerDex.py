from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from trainerdex.api.exceptions import Forbidden
from trainerdex.api.http.base import BaseHTTPClient

P = ParamSpec("P")
T = TypeVar("T")


def requires_authentication(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator for methods that require authentication."""

    @wraps(func)
    def wrapper(self: BaseHTTPClient, *args, **kwargs) -> T:
        if not self.authenticated:
            raise Forbidden("This method requires authentication.")
        return func(self, *args, **kwargs)

    return wrapper
