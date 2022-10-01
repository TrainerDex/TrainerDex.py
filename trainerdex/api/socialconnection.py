from __future__ import annotations

import json
from typing import Any, Dict, Union

from trainerdex.api.base import BaseClass
from trainerdex.api.trainer import Trainer
from trainerdex.api.utils import convert


class SocialConnection(BaseClass):
    def _update(self, data: Dict[str, Union[str, int]]) -> None:
        self._user_id: int = data.get("user")
        self._user = None
        self.provider: str = data.get("provider")
        self.uid: str = data.get("uid")
        self.extra_data: Any = convert(json.loads, data.get("extra_data"))
        self._trainer_id: int = data.get("trainer")
        self._trainer = None

    def __eq__(self, other) -> bool:
        if isinstance(other, SocialConnection):
            return self.provider == other.provider and self.uid == other.uid
        else:
            raise TypeError("Cannot compare SocialConnection with other types")

    def __hash__(self):
        return hash((self.provider, self.uid))

    async def get_user(self):
        if not self._user:
            self._user = await self.client.get_user(self._user_id)

        return self._user

    async def get_trainer(self) -> Trainer:
        if not self._trainer:
            self._trainer = await self.client.get_trainer(self._trainer_id)

        return self._trainer

    async def refresh_from_api(self) -> None:
        data = await self.client.get_social_connections(self.provider, self.uid)
        self._update(data[0])
