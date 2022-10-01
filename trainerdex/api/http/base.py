from __future__ import annotations

import asyncio
import os
import sys
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Coroutine,
    Dict,
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

    def __init__(self, token: str = None, loop=None) -> None:
        self.loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()
        self.token: str = token

        user_agent = (
            "TrainerDex.py (https://github.com/TrainerDex/TrainerDex.py {0}) "
            "Python/{1} "
            "aiohttp/{2}"
        )
        self.user_agent = user_agent.format(__version__, sys.version, aiohttp_version)

    def __enter__(self) -> None:
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

    def _create_session(self) -> ClientSession:
        return ClientSession(base_url=self.HOST, headers=self.headers)

    @property
    def headers(self) -> Dict:
        headers = {
            "User-Agent": self.user_agent,
        }

        if self.token is not None:
            headers["Authorization"] = f"Token {self.token}"

        return headers

    @property
    def session(self) -> ClientSession:
        maybe_session: Union[ClientSession, None] = getattr(self, "_session", None)
        if isinstance(maybe_session, ClientSession) and not maybe_session.closed:
            return maybe_session
        else:
            raise RuntimeError("Session is not open. Please use an async with context manager.")

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
