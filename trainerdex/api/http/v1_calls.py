from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Iterable, List, Literal, Optional, Union
from uuid import UUID

from trainerdex.api.http.auth.decorators import requires_authentication
from trainerdex.api.http.base import BaseHTTPClient

if TYPE_CHECKING:
    from trainerdex.api.http.base import Response
    from trainerdex.api.types.v1.social_connection import (
        CreateSocialConnection,
        ReadSocialConnection,
    )
    from trainerdex.api.types.v1.trainer import CreateTrainer, EditTrainer, ReadTrainer
    from trainerdex.api.types.v1.update import CreateUpdate, EditUpdate, ReadUpdate
    from trainerdex.api.types.v1.user import CreateUser, ReadUser

    StrOrUUID = Union[str, UUID]


class APIV1Mixin(BaseHTTPClient):
    """Holds the API calls for the v1 API."""

    def _v1_get_update(self, trainer_id: int, uuid: StrOrUUID) -> Response[ReadUpdate]:
        return self.request("GET", f"/api/v1/trainers/{trainer_id}/updates/{uuid}/")

    def _v1_get_updates_for_trainer(self, trainer_id: int) -> Response[List[ReadUpdate]]:
        return self.request("GET", f"/api/v1/trainers/{trainer_id}/updates/")

    @requires_authentication
    def _v1_create_update(self, trainer_id: int, payload: CreateUpdate) -> Response[ReadUpdate]:
        return self.request("POST", f"/api/v1/trainers/{trainer_id}/updates/", json=payload)

    @requires_authentication
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

    @requires_authentication
    def _v1_create_trainer(self, payload: CreateTrainer) -> Response[ReadTrainer]:
        return self.request("POST", "/api/v1/trainers/", json=payload)

    @requires_authentication
    def _v1_edit_trainer(self, trainer_id: int, payload: EditTrainer) -> Response[ReadTrainer]:
        return self.request("PATCH", f"/api/v1/trainers/{trainer_id}/", json=payload)

    def _v1_get_user(self, user_id: int) -> Response[ReadUser]:
        return self.request("GET", f"/api/v1/users/{user_id}/")

    def _v1_get_users(self) -> Response[List[ReadUser]]:
        return self.request("GET", "/api/v1/users/")

    @requires_authentication
    def _v1_create_user(self, payload: CreateUser) -> Response[ReadUser]:
        return self.request("POST", "/api/v1/users/", json=payload)

    @requires_authentication
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

    @requires_authentication
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
