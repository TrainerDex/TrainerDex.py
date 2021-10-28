import datetime
from typing import Callable, Dict, Iterator, List, Optional, Union
from warnings import warn

from dateutil.parser import parse

from . import abc
from .faction import Faction
from .http import HTTPClient
from .trainer import Trainer
from .utils import con, maybe_coroutine


class LeaderboardEntry(abc.BaseClass):
    def __init__(self, conn: HTTPClient, data: Dict[str, Union[str, int, float]]) -> None:
        super().__init__(conn, data)
        self._trainer = None

    def _update(self, data: Dict[str, Union[str, int, float]]) -> None:
        self.level = data.get("level")
        self.position = data.get("position", None)
        self._trainer_id = data.get("id", None)
        self.username = data.get("username")
        self._faction = data.get("faction", {"id": 0, "name_en": "No Team"})
        self.value = data.get("value", 0)
        self.update_time = con(parse, data.get("last_updated"))
        self._user_id = data.get("user_id", None)

    @property
    def faction(self) -> Faction:
        return Faction(self._faction.get("id"))

    @property
    def total_xp(self) -> Optional[int]:
        warn(
            "LeaderboardEntry.total_xp is deprecated. It will be removed in version 4.0",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._total_xp

    @property
    def last_updated(self) -> Optional[datetime.datetime]:
        return self.update_time

    async def trainer(self) -> Trainer:
        if self._trainer:
            return self._trainer

        data = await self.http.get_trainer(self._trainer_id)
        self._trainer = Trainer(conn=self.http, data=data)

        return self._trainer


class Aggregations:
    def __init__(self, data: Dict[str, Union[int, float]]) -> None:
        self.avg = data.get("avg")
        self.count = data.get("count")
        self.min = data.get("min")
        self.max = data.get("max")
        self.sum = data.get("sum")

    def __len__(self) -> int:
        return self.count

    def __length_hint__(self) -> int:
        return self.__len__()


class BaseLeaderboard:
    def __init__(self, conn: HTTPClient, data: Dict[str, Union[str, int]]) -> None:
        self.http = conn
        self.i = 0
        self._entries = data.get("leaderboard")
        self.title = data.get("title", "Global Leaderboard")
        self.stat = data.get("stat")
        self._aggregations = data.get("aggregations", dict())
        self.aggregations = Aggregations(self._aggregations)
        self.avg = self._aggregations.get("avg")
        self.count = self._aggregations.get("count")
        self.min = self._aggregations.get("min")
        self.max = self._aggregations.get("max")
        self.sum = self._aggregations.get("sum")

    def __aiter__(self):
        return self

    async def __anext__(self) -> LeaderboardEntry:
        i = self.i
        if i >= len(self._entries):
            raise StopAsyncIteration
        self.i += 1
        return LeaderboardEntry(conn=self.http, data=self._entries[i])

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
            LeaderboardEntry(conn=self.http, data=x)
            for x in self._entries
            if x.get("position") == key
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
            x for x in self._entries if predicate(LeaderboardEntry(conn=self.http, data=x))
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


class Leaderboard(BaseLeaderboard):
    pass


class GuildLeaderboard(BaseLeaderboard):
    def __init__(self, conn: HTTPClient, data: Dict[str, Union[str, int, float]]) -> None:
        super().__init__(conn, data)
        self.guild_id = data.get("guild")


class CommunityLeaderboard(BaseLeaderboard):
    def __init__(self, conn: HTTPClient, data: Dict[str, Union[str, int, float]]) -> None:
        super().__init__(conn, data)
        self.community = data.get("community")


class CountryLeaderboard(BaseLeaderboard):
    def __init__(self, conn: HTTPClient, data: Dict[str, Union[str, int, float]]) -> None:
        super().__init__(conn, data)
        self.country = data.get("country")
        self.country_code = self.country
        self.country_name = self.title.replace(" Leaderboard", "")
