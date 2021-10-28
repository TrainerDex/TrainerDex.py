import asyncio
import datetime
import logging
from typing import Iterable, List, Optional, Union
from uuid import UUID

from .faction import Faction
from .http import HTTPClient
from .leaderboard import CommunityLeaderboard, CountryLeaderboard, GuildLeaderboard, Leaderboard
from .socialconnection import SocialConnection
from .trainer import Trainer
from .update import Update
from .user import User

log: logging.Logger = logging.getLogger(__name__)


class Client:
    def __init__(self, token: str = None, loop=None) -> None:
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.http = HTTPClient(token=token, loop=self.loop)

    async def get_trainer(self, trainer_id: int) -> Trainer:
        data = await self.http.get_trainer(trainer_id)
        trainer = Trainer(conn=self.http, data=data)
        await trainer.fetch_updates()
        return trainer

    async def create_trainer(
        self,
        username: str,
        faction: Union[int, Faction],
        start_date: Optional[datetime.date] = None,
        trainer_code: Optional[str] = None,
        is_banned: bool = False,
        is_verified: bool = True,
        is_visible: bool = True,
        first_name: Optional[str] = None,
        user: Optional[User] = None,
    ) -> Trainer:
        """Creates Trainer

        If :parameter:`user` is None, it will create a user. This is the default behavour!
        """
        if user is None:
            u_params = {"username": username, "first_name": first_name}
            u_data = await self.http.create_user(**u_params)
            user = User(conn=self.http, data=u_data)

        assert isinstance(user, User)

        t_params = {
            "id": user.id,
            "nickname": username,
            "faction": faction.id if isinstance(faction, Faction) else faction,
            "start_date": start_date.isoformat() if start_date else None,
            "trainer_code": trainer_code,
            "is_banned": is_banned,
            "is_verified": is_verified,
            "is_visible": is_visible,
        }
        t_data = await self.http.create_trainer(**t_params)
        t_data["_user"] = User
        trainer = Trainer(conn=self.http, data=t_data)
        await trainer.fetch_updates()
        return trainer

    async def get_trainers(self) -> Iterable[Trainer]:
        data = await self.http.get_trainers()
        return [Trainer(conn=self.http, data=x) for x in data]

    async def get_user(self, user_id: int) -> User:
        data = await self.http.get_user(user_id)
        return User(conn=self.http, data=data)

    async def get_users(self) -> Iterable[User]:
        data = await self.http.get_users()
        return tuple(User(conn=self.http, data=x) for x in data)

    async def get_update(self, update_uuid: Union[str, UUID]) -> Update:
        data = await self.http.get_update(update_uuid)
        return Update(conn=self.http, data=data)

    async def get_social_connections(
        self, provider: str, uid: Union[str, Iterable[str]]
    ) -> List[SocialConnection]:
        data = await self.http.get_social_connections(provider, uid)
        return [SocialConnection(conn=self.http, data=x) for x in data]

    async def get_leaderboard(
        self,
        stat: str = "total_xp",
        guild=None,
        community: Optional[str] = None,
        country: Optional[str] = None,
    ) -> Union[Leaderboard, GuildLeaderboard, CommunityLeaderboard, CountryLeaderboard]:
        if guild:
            if isinstance(guild, int):
                guild_id = guild
            else:
                guild_id = guild.id
            leaderboard_class = GuildLeaderboard
        elif community:
            leaderboard_class = CommunityLeaderboard
        elif country:
            leaderboard_class = CountryLeaderboard
        else:
            guild_id = None
            leaderboard_class = Leaderboard
        data = await self.http.get_leaderboard(stat=stat, guild_id=guild_id)
        return leaderboard_class(conn=self.http, data=data)

    async def search_trainer(self, nickname: str) -> Trainer:
        """Searches for a trainer with a certain nickname

        Parameters
        ----------

            nickname: :class:str
                The nickname of the trainer you want to search for.
                This search is case insensitive.

        Returns
        -------

            :class:trainerdex.Trainer

        Raises
        ------

            :class:NotFound

        """

        queryset = await self.http.get_trainers(q=nickname)

        if len(queryset) == 1:
            return Trainer(conn=self.http, data=queryset[0])
        else:
            raise IndexError
