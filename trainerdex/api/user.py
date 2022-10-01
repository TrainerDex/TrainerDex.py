from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from trainerdex.api.base import BaseClass
from trainerdex.api.socialconnection import SocialConnection
from trainerdex.api.trainer import Trainer
from trainerdex.api.types.v1.social_connection import CreateSocialConnection
from trainerdex.api.utils import HasID

if TYPE_CHECKING:
    from trainerdex.api.types.v1.user import ReadUser


class User(BaseClass):
    def _update(self, data: ReadUser) -> None:
        self.id = data["id"]
        self.uuid = data["uuid"]
        self.username = data["username"]
        self.trainer_id = data["trainer"]

    async def get_trainer(self) -> Trainer:
        if not self._trainer:
            self._trainer = await self.client.get_trainer(self.trainer_id)

        return self._trainer

    async def refresh_from_api(self) -> None:
        data = await self.client._v1_get_user(self.id)
        self._update(data)

    async def add_social_connection(
        self, provider: str, uid: str, extra_data: Optional[Dict] = None
    ) -> SocialConnection:
        payload = CreateSocialConnection(
            user=self.id,
            provider=provider,
            uid=uid,
            extra_data=extra_data,
        )
        data = await self.client._v1_create_social_connection(payload)
        return SocialConnection(data=data, client=self.client)

    async def add_discord(self, discord: HasID) -> SocialConnection:
        return await self.add_social_connection(provider="discord", uid=str(discord.id))
