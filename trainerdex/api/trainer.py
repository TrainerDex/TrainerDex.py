from __future__ import annotations

import datetime
import re
from typing import TYPE_CHECKING, Dict, List, Optional
from uuid import UUID as _UUID

from dateutil.parser import parse

from trainerdex.api.base import BaseClass
from trainerdex.api.faction import Faction
from trainerdex.api.types.v1.update import CreateUpdate
from trainerdex.api.types.v1.update import Update as StatsPayload
from trainerdex.api.update import Update
from trainerdex.api.utils import convert

if TYPE_CHECKING:
    from trainerdex.api.types.v1.trainer import ReadTrainer

parse_dt = convert(parse)
UUID = convert(_UUID)


class Trainer(BaseClass):
    def _update(self, data: ReadTrainer) -> None:
        self.id = data["id"]
        self.uuid = UUID(data["uuid"])
        self.created_at = parse_dt(data["created_at"])
        self.updated_at = parse_dt(data["updated_at"])
        self.last_modified = parse_dt(data["last_modified"])
        self.username = data["username"]
        self.user_id = data["owner"]
        self.start_date = None
        if data["start_date"]:
            start_datetime = parse_dt(data["start_date"])
            if start_datetime is not None:
                self.start_date = start_datetime.date()

        self.faction = data["faction"]
        self.trainer_code = data["trainer_code"]
        self.last_cheated = parse_dt(data["last_cheated"])
        self.daily_goal = data["daily_goal"]
        self.total_goal = data["total_goal"]
        self.verified = data["verified"]
        self.statistics = data["statistics"]
        self.prefered = data["prefered"]
        self._updates = []
        self._user = None

    @property
    def team(self) -> Faction:
        return Faction(self.faction)

    async def fetch_updates(self) -> None:
        data = await self.client._v1_get_updates_for_trainer(self.id)
        if data:
            self._updates = [Update(self.client, update) for update in data]

    @property
    def updates(self) -> List[Update]:
        return self._updates.copy()

    async def get_latest_update(self) -> Update:
        if not self.updates:
            await self.fetch_updates()

        return max(self.updates, key=lambda x: x.update_time)

    async def get_level(self) -> int:
        if not self.updates:
            await self.fetch_updates()

        subset = [update for update in self.updates if update.trainer_level]
        return max(subset, key=lambda x: x.update_time).trainer_level

    async def get_user(self):
        if self._user is None:
            self._user = await self.client.get_user(self.user_id)

        return self._user

    async def refresh_from_api(self) -> None:
        data = await self.client.get_trainer(self.old_id)
        self._update(data)

    async def edit(self, **payload) -> None:
        """|coro|

        Edits the current trainer

        .. note::
            Changing username is currently unsupported with the current API level.
            Changing IDs is forever unsupported

        Parameters
        -----------
        start_date: :class:`datetime.datetime`
            The date the Trainer started playing Pokemon Go
        faction: Union[:class:`Faction`, :class:`int`]
            The team the Trainer belongs to
        trainer_code: Union[:class:`int`, :class:`int`]
            The Trainer's Trainer/Friend code, this will be processed to remove any whitespace
        is_verified: :class:`bool`
            If the Trainer's information has been looked at and approved.
        is_visible: :class:`bool`
            If the Trainer has given consent for their data to be shared.

        Raises
        ------
        HTTPException
            Editing your profile failed.
        """

        if isinstance(payload.get("start_date"), Faction):
            payload["start_date"] = payload["start_date"].isoformat()

        if isinstance(payload.get("faction"), Faction):
            payload["faction"] = payload["faction"].id

        if payload.get("trainer_code"):
            payload["trainer_code"] = re.sub(
                r"\s+", "", str(payload["trainer_code"]), flags=re.UNICODE
            )

        new_data = await self.client._v1_edit_trainer(self.id, payload)
        self._update(new_data)

    async def post(
        self,
        data_source: str,
        stats: StatsPayload,
        update_time: Optional[datetime.datetime] = None,
    ) -> Update:
        """|coro|

        Posts an update on the current trainer

        .. note::
            This will refresh the Trainer instance too
        """
        payload = CreateUpdate(
            trainer=self.id,
            data_source=data_source,
            **stats,
        )
        if update_time is not None:
            payload["update_time"] = update_time.isoformat()

        data = await self.client._v1_create_update(self.id, payload)
        result = Update(self.client, data)
        return result
