import datetime
import re
from typing import Dict, List, Union

from dateutil.parser import parse

from . import abc
from .faction import Faction
from .http import TRAINER_KEYS_ENUM_IN, HTTPClient
from .update import Level, Update
from .utils import con

odt = con(parse)


class Trainer(abc.BaseClass):
    def __init__(self, conn: HTTPClient, data: Dict[str, Union[str, int]]) -> None:
        super().__init__(conn, data)

    def _update(self, data: Dict[str, Union[str, int]]) -> None:
        data = {
            TRAINER_KEYS_ENUM_IN.get(k): v
            for k, v in data.items()
            if (TRAINER_KEYS_ENUM_IN.get(k) is not None)
        }
        self.id = int(data.get("id"))
        self.username = data.get("nickname")
        self.old_id = int(data.get("old_id"))
        self.last_modified = odt(data.get("last_modified"))
        self.nickname = data.get("nickname")
        self.start_date = odt(data.get("start_date")).date() if data.get("start_date") else None
        self.faction = data.get("faction", 0)
        self.trainer_code = data.get("trainer_code")
        self.is_banned = data.get("is_banned", False)
        self.is_verified = data.get("is_verified")
        self.is_visible = data.get("is_visible")
        self._updates = dict()
        self._user = data.get("_user")

    def __eq__(self, o) -> bool:
        return self.old_id == o.old_id

    def __hash__(self):
        return hash(self.id)

    @property
    def team(self) -> Faction:
        return Faction(self.faction)

    async def fetch_updates(self) -> None:
        trainer_id = self.old_id
        data = await self.http.get_updates_for_trainer(trainer_id)
        if data:
            self._updates = {x.get("uuid"): Update(self.http, x) for x in data}
            return list(self._updates.values())

    @property
    def updates(self) -> List[Update]:
        return list(self._updates.values())

    def get_latest_update_for_stat(self, stat) -> Update:
        subset = [x for x in self.updates if getattr(x, stat, None) is not None]
        return max(subset, key=lambda x: x.update_time)

    def get_latest_update(self) -> Update:
        return max(self.updates, key=lambda x: x.update_time)

    @property
    def level(self) -> Level:
        update = self.get_latest_update_for_stat("total_xp")
        if update:
            return update.level

    async def user(self):
        if self._user:
            return self._user

        # have to import User late to prevent circular imports
        from .user import User

        data = await self.http.get_user(self.id)
        self._user = User(data=data, conn=self.http)

        return self._user

    async def refresh_from_api(self) -> None:
        data = await self.http.get_trainer(self.old_id)
        self._update(data)

    async def edit(self, **options) -> None:
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

        if isinstance(options.get("start_date"), Faction):
            options["start_date"] = options["start_date"].isoformat()

        if isinstance(options.get("faction"), Faction):
            options["faction"] = options["faction"].id

        if options.get("trainer_code"):
            options["trainer_code"] = re.sub(
                r"\s+", "", str(options["trainer_code"]), flags=re.UNICODE
            )

        new_data = await self.http.edit_trainer(self.old_id, **options)
        self._update(new_data)

    async def post(
        self,
        data_source: str,
        stats: Dict,
        update_time: datetime.datetime = None,
        submission_date: datetime.datetime = None,
    ) -> Update:
        """|coro|

        Posts an update on the current trainer

        .. note::
            This will refresh the Trainer instance too
        """
        trainer_id = self.old_id

        options = {"trainer": trainer_id, "data_source": data_source}
        if update_time:
            options["update_time"] = update_time
        if submission_date:
            options["submission_date"] = submission_date

        data = await self.http.create_update(trainer_id, {**options, **stats})
        result = Update(data=data, conn=self.http)
        await self.refresh_from_api()
        return result
