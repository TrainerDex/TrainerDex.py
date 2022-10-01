from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, Iterator, List, Optional, Union

from dateutil.parser import parse

from trainerdex.api.base import BaseClass
from trainerdex.api.faction import Faction
from trainerdex.api.trainer import Trainer
from trainerdex.api.utils import convert, maybe_coroutine


class LeaderboardEntry(BaseClass):
    def _update(self, data: Dict[str, Union[str, int, float]]) -> None:
        self.level: Optional[int] = data.get("level")
        self.position: int = data["position"]
        self.trainer_id: int = data["id"]
        self.username: str = data["username"]
        self.faction_id: Optional[int] = data.get("faction", {}).get("id")
        self.value = data["value"]
        self.update_time = convert(parse, data.get("last_updated"))

    def refresh_from_api(self) -> None:
        ...

    @property
    def faction(self) -> Union[Faction, None]:
        if self.faction_id:
            return Faction(self.faction_id)

    @property
    def last_updated(self) -> Optional[datetime.datetime]:
        return self.update_time

    async def get_trainer(self) -> Trainer:
        if getattr(self, "_trainer", None) is None:
            self._trainer = await self.client.get_trainer(self.trainer_id)

        return self._trainer

    def __eq__(self, other) -> bool:
        raise object.__eq__(self, other)

    def __hash__(self):
        return object.__hash__(self)


class Aggregations:
    def __init__(self, data: Dict[str, Union[int, float]]) -> None:
        self.avg = data.get("avg", 0)
        self.count = data.get("count", 0)
        self.min = data.get("min", 0)
        self.max = data.get("max", 0)
        self.sum = data.get("sum", 0)

    def __len__(self) -> int:
        return self.count

    def __length_hint__(self) -> int:
        return self.__len__()


class BaseLeaderboard(BaseClass):
    def _update(self, data: Dict[str, Any]) -> None:
        self.index = 0
        self._entries: List[Dict] = data["leaderboard"]
        self.title: str = data.get("title", "Global Leaderboard")
        self.stat: str = data.get("stat")
        self._aggregations: Dict = data.get("aggregations", {})
        self.aggregations = Aggregations(self._aggregations)

    def refresh_from_api(self) -> None:
        ...

    def __aiter__(self):
        return self

    async def __anext__(self) -> LeaderboardEntry:
        index = self.index
        if index >= len(self._entries):
            raise StopAsyncIteration
        self.index += 1
        return LeaderboardEntry(client=self.client, data=self._entries[index])

    def __len__(self) -> int:
        return self.aggregations.count

    def __length_hint__(self) -> int:
        return self.__len__()

    def __getitem__(self, key) -> List[LeaderboardEntry]:
        """Retrieves a list of :class:`.LeaderboardEntry` in a position.

        .. note::

            There can be multiple :class:`.LeaderboardEntry` for a position.
            This happens when they both have the same stat.
        """
        return [
            LeaderboardEntry(client=self.client, data=entry)
            for entry in self._entries
            if entry.get("position") == key
        ]

    def filter(self, predicate) -> Iterator[LeaderboardEntry]:
        """Filter the iterable with an (optionally async) predicate.

        Parameters
        ----------
        function: Callable
            A function or coroutine function which takes one item of ``iterable``
            as an argument, and returns ``True`` or ``False``.

        Returns
        -------
            An object which can either be awaited to yield a list of the filtered
            items, or can also act as an async iterator to yield items one by one.

        Examples
        --------
        >>> from tdx.leaderboard import Leaderboard
        >>> def predicate(value):
        ...     return value.faction.id == 0
        >>> iterator = Leaderboard()
        >>> async for i in iterator.filter(predicate):
        ...     print(i)


        >>> from redbot.core.utils import AsyncIter
        >>> def predicate(value):
        ...     return value.level.level < 5
        >>> iterator = AsyncIter([1, 10, 5, 100])
        >>> await iterator.filter(predicate)
        [1, 5]

        """
        self._entries = [
            x for x in self._entries if predicate(LeaderboardEntry(client=self.client, data=x))
        ]
        return self

    async def find(
        self, predicate: Callable, default: Optional[LeaderboardEntry] = None
    ) -> LeaderboardEntry:
        """Calls ``predicate`` over items in iterable and return first value to match.

        Parameters
        ----------
        predicate: Union[Callable, Coroutine]
            A function that returns a boolean-like result. The predicate provided can be a coroutine.
        default: Optional[Any]
            The value to return if there are no matches.

        Raises
        ------
        TypeError
            When ``predicate`` is not a callable.

        Examples
        --------
        >>> from tdx.leaderboard import Leaderboard
        >>> await Leaderboard().find(lambda x: x.trainer.id == 1)
        <LeaderboardEntry>
        """
        while True:
            try:
                elem = await self.__anext__()
            except StopAsyncIteration:
                return default
            ret = await maybe_coroutine(predicate, elem)
            if ret:
                return elem

    def __eq__(self, other) -> bool:
        raise object.__eq__(self, other)

    def __hash__(self):
        return object.__hash__(self)


class Leaderboard(BaseLeaderboard):
    pass


class GuildLeaderboard(BaseLeaderboard):
    def _update(self, data: Dict[str, Any]) -> None:
        super()._update(data)
        self.guild_id = data.get("guild")


class CommunityLeaderboard(BaseLeaderboard):
    def _update(self, data: Dict[str, Any]) -> None:
        super()._update(data)
        self.community = data.get("community")


class CountryLeaderboard(BaseLeaderboard):
    def _update(self, data: Dict[str, Any]) -> None:
        super()._update(data)
        self.country = data.get("country")
        self.country_code = self.country
        self.country_name = self.title.replace(" Leaderboard", "")
