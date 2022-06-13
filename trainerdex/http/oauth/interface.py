from __future__ import annotations

import asyncio
import os
import sys
import weakref
from abc import abstractmethod
from typing import TYPE_CHECKING

import aiohttp
from promise import promisify
import ujson

from trainerdex.http.interface import iHTTPClient
from trainerdex.version import __version__

if TYPE_CHECKING:
    from typing_extensions import Self


class iOAuthClient(iHTTPClient):
    ORIGIN = os.environ.get("TRAINERDEX_ORIGIN", "https://trainerdex.app")

    def __init__(self, loop: asyncio.AbstractEventLoop = None) -> None:
        self._loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            base_url=self.ORIGIN,
            loop=self._loop,
            headers={"User-Agent": self.user_agent},
            json_serialize=ujson.dumps,
        )
        self._finalizer = weakref.finalize(self, self.close)

    @promisify
    async def close(self) -> None:
        await self.session.close()

    def __enter__(self) -> None:
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.close()

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def user_agent(self) -> str:
        user_agent = (
            "TrainerDex.py (https://github.com/TrainerDex/TrainerDex.py {0}) "
            "Python/{1} "
            "aiohttp/{2}"
        )
        return user_agent.format(__version__, sys.version, aiohttp.__version__)

    @abstractmethod
    def authenticate(self, client_id: str, client_secret: str, *args, **kwargs):
        ...
