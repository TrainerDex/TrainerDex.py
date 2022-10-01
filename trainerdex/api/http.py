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
    Iterable,
    List,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
)
from typing_extensions import Self
from uuid import UUID

from aiohttp import ContentTypeError
from aiohttp import __version__ as aiohttp_version
from aiohttp.client import ClientSession
from aiohttp.typedefs import StrOrURL

if TYPE_CHECKING:
    from .types.v1.social_connection import CreateSocialConnection, ReadSocialConnection
    from .types.v1.trainer import CreateTrainer, EditTrainer, ReadTrainer
    from .types.v1.update import CreateUpdate, EditUpdate, ReadUpdate
    from .types.v1.user import CreateUser, ReadUser

    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]
    StrOrUUID = Union[str, UUID]


from . import __version__
from .exceptions import Forbidden, HTTPException, NotFound


class HTTPClient:
    """Represents an HTTP client sending HTTP requests to the TrainerDex API."""

    HOST: ClassVar[str] = os.environ.get("TRAINERDEX_HOST", "https://trainerdex.app/")

    def __init__(self, token: str = None, loop=None) -> None:
        self.loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()
        self.token: str = token

        user_agent = (
            "TrainerDex.py (https://github.com/TrainerDex/TrainerDex.py {0}) "
            "Python/{1[0]}.{1[1]} "
            "aiohttp/{2}"
        )
        self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp_version)

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

    def _v1_get_update(self, trainer_id: int, uuid: StrOrUUID) -> Response[ReadUpdate]:
        return self.request("GET", f"/api/v1/trainers/{trainer_id}/updates/{uuid}/")

    def _v1_get_updates_for_trainer(self, trainer_id: int) -> Response[List[ReadUpdate]]:
        return self.request("GET", f"/api/v1/trainers/{trainer_id}/updates/")

    def _v1_create_update(self, trainer_id: int, payload: CreateUpdate) -> Response[ReadUpdate]:
        return self.request("POST", f"/api/v1/trainers/{trainer_id}/updates/", json=payload)

    def _v1_edit_update(
        self, trainer_id: int, update_uuid: StrOrUUID, payload: EditUpdate
    ) -> Response[ReadUpdate]:
        payload["trainer"] = trainer_id
        return self.request(
            "PATCH", f"/api/v1/trainers/{trainer_id}/updates/{update_uuid}/", json=payload
        )

    def _v1_get_trainer(self, trainer_id: int) -> Response[ReadTrainer]:
        return self.request("GET", f"/api/v1/trainers/{trainer_id}/")

    def _v1_get_trainers(
        self, *, t: Literal[0, 1, 2, 3] = None, q: str = None
    ) -> Response[List[ReadTrainer]]:
        params = {}
        if t is not None:
            params["t"] = t
        if q is not None:
            params["q"] = q

        return self.request("GET", "/api/v1/trainers/", params=params)

    def _v1_create_trainer(self, payload: CreateTrainer) -> Response[ReadTrainer]:
        return self.request("POST", "/api/v1/trainers/", json=payload)

    def _v1_edit_trainer(self, trainer_id: int, payload: EditTrainer) -> Response[ReadTrainer]:
        return self.request("PATCH", f"/api/v1/trainers/{trainer_id}/", json=payload)

    def _v1_get_user(self, user_id: int) -> Response[ReadUser]:
        return self.request("GET", f"/api/v1/users/{user_id}/")

    def _v1_get_users(self) -> Response[List[ReadUser]]:
        return self.request("GET", "/api/v1/users/")

    def _v1_create_user(self, payload: CreateUser) -> Response[ReadUser]:
        return self.request("POST", "/api/v1/users/", json=payload)

    def _v1_get_social_connections(
        self,
        uid: Union[str, Iterable[str]],
        provider: Literal["discord"] = "discord",
    ) -> Response[List[ReadSocialConnection]]:
        if isinstance(uid, str):
            uid = [uid]
        else:
            uid = list(uid)

        return self.request(
            "GET",
            "/api/v1/users/social/",
            params={
                "uid": ",".join(uid),
                "provider": provider,
            },
        )

    def _v1_create_social_connection(
        self, payload: CreateSocialConnection
    ) -> Response[ReadSocialConnection]:
        return self.request("POST", "/api/v1/users/social/", json=payload)

    def _v1_get_leaderboard(
        self,
        stat: str = "total_xp",
        guild_id: Optional[int] = None,
        community: Optional[str] = None,
        country: Optional[str] = None,
    ) -> Response[Dict]:
        if guild_id:
            endpoint = f"/api/v1/leaderboard/discord/{guild_id}/"
        elif community:
            endpoint = f"/api/v1/leaderboard/community/{community}/"
        elif country:
            endpoint = f"/api/v1/leaderboard/country/{country}/"
        else:
            endpoint = "/api/v1/leaderboard/v1.1/"

        if stat:
            endpoint += f"{stat}/"

        return self.request("GET", endpoint)
