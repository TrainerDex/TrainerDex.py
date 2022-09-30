from typing import Dict, Optional, Union

from .base import BaseClass
from .http import HTTPClient
from .socialconnection import SocialConnection
from .trainer import Trainer


class User(BaseClass):
    def __init__(self, client: HTTPClient, data: Dict[str, Union[str, int]]) -> None:
        super().__init__(client, data)
        self._trainer = None

    def _update(self, data: Dict[str, Union[str, int]]) -> None:
        self.id = int(data.get("id"))
        self.username = data.get("username")
        self.first_name = data.get("first_name")
        self.old_id = int(data.get("trainer"))

    def __eq__(self, o) -> bool:
        return self.id == o.id

    def __hash__(self):
        return hash(self.id)

    async def trainer(self) -> Trainer:
        if self._trainer:
            return self._trainer

        data = await self.client.get_trainer(self.old_id)
        self._trainer = Trainer(data=data, conn=self.client)
        await self._trainer.fetch_updates()

        return self._trainer

    async def refresh_from_api(self) -> None:
        data = await self.client.get_user(self.id)
        self._update(data)

    async def add_social_connection(
        self, provider: str, uid: str, extra_data: Optional[Dict] = None
    ) -> SocialConnection:
        data = await self.client.create_social_connection(
            user=self.id, provider=provider, uid=uid, extra_data=extra_data
        )
        return SocialConnection(data=data, client=self.client)

    async def add_discord(self, discord) -> SocialConnection:
        return await self.add_social_connection("discord", str(discord.id))
