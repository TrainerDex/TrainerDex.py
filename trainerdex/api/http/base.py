from __future__ import annotations

import asyncio
import os
import sys
from abc import abstractclassmethod
from types import MappingProxyType, TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Coroutine,
    Dict,
    NoReturn,
    Optional,
    Type,
    TypeVar,
    Union,
)

from aiohttp import ContentTypeError
from aiohttp import __version__ as aiohttp_version
from aiohttp.client import ClientSession
from aiohttp.typedefs import StrOrURL
from typing_extensions import Self

from trainerdex.api import __version__
from trainerdex.api.exceptions import Forbidden, HTTPException, NotFound

if TYPE_CHECKING:
    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]


class BaseHTTPClient:
    """Represents an HTTP client sending HTTP requests to the TrainerDex API."""

    HOST: ClassVar[str] = os.environ.get("TRAINERDEX_HOST", "https://trainerdex.app/")

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()
        self._headers: Dict[str, str] = {
            "User-Agent": self.user_agent,
        }
        self._authenticated: bool = False

    @property
    def user_agent(self) -> str:
        user_agent = (
            "TrainerDex.py (https://github.com/TrainerDex/TrainerDex.py {0}) "
            "Python/{1} "
            "aiohttp/{2}"
        )
        return user_agent.format(__version__, sys.version, aiohttp_version)

    @property
    def authenticated(self) -> bool:
        return self._authenticated

    @property
    def headers(self) -> MappingProxyType[str, str]:
        return MappingProxyType(self._headers)

    def _create_session(self) -> ClientSession:
        return ClientSession(
            base_url=self.HOST,
            headers=self.headers,
            loop=self.loop,
        )

    @property
    def session(self) -> ClientSession:
        maybe_session: Union[ClientSession, None] = getattr(self, "_session", None)
        if isinstance(maybe_session, ClientSession) and not maybe_session.closed:
            return maybe_session
        else:
            raise RuntimeError("Session is not open. Please use an async context manager.")

    async def request(self, method: str, path: StrOrURL, **kwargs) -> Any:
        async with self.session.request(method, path, **kwargs) as response:
            try:
                data = await response.json()
            except ContentTypeError:
                data = await response.text()
            except Exception:
                data = None

            if response.ok:
                return data
            elif response.status in {401, 403, 423}:
                raise Forbidden(response, data)
            elif response.status == 404:
                raise NotFound(response, data)
            else:
                raise HTTPException(response, data)

    @abstractclassmethod
    def authenticate(self, **credentials) -> Union[Self, Coroutine[Any, Any, Self]]:
        """Authenticate with the TrainerDex API.

        Takes in credentials and modifies the headers on the client to include the authentication token.

        Returns self for chaining.
        May be a coroutine.
        """
        self._authenticated = True
        return self

    def __enter__(self) -> NoReturn:
        raise TypeError("Use async with instead")

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        # __exit__ should exist in pair with __enter__ but never executed
        pass

    async def __aenter__(self) -> Self:
        self._session = self._create_session()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._session.close()
