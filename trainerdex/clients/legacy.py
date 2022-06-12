import datetime
import logging
from typing import Iterable, List, Optional, Union
from uuid import UUID

from promise import promisify

from trainerdex.faction import Faction
from trainerdex.http.bearer import BearerHTTPClient
from trainerdex.leaderboard import (
    CommunityLeaderboard,
    CountryLeaderboard,
    GuildLeaderboard,
    Leaderboard,
)
from trainerdex.socialconnection import SocialConnection
from trainerdex.trainer import Trainer
from trainerdex.update import Update
from trainerdex.user import User

log: logging.Logger = logging.getLogger(__name__)


class LegacyClient(BearerHTTPClient):
    @promisify
    async def get_trainer(self, trainer_id: int) -> Trainer:
        data = await self.get_trainer(trainer_id)
        trainer = Trainer(conn=self, data=data)
        await trainer.fetch_updates()
        return trainer

    @promisify
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
            u_data = await self.create_user(**u_params)
            user = User(conn=self, data=u_data)

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
        t_data = await self.create_trainer(**t_params)
        t_data["_user"] = User
        trainer = Trainer(conn=self, data=t_data)
        await trainer.fetch_updates()
        return trainer

    @promisify
    async def get_trainers(self) -> Iterable[Trainer]:
        data = await self.get_trainers()
        return [Trainer(conn=self, data=x) for x in data]

    @promisify
    async def get_user(self, user_id: int) -> User:
        data = await self.get_user(user_id)
        return User(conn=self, data=data)

    @promisify
    async def get_users(self) -> Iterable[User]:
        data = await self.get_users()
        return tuple(User(conn=self, data=x) for x in data)

    @promisify
    async def get_update(self, update_uuid: Union[str, UUID]) -> Update:
        data = await self.get_update(update_uuid)
        return Update(conn=self, data=data)

    @promisify
    async def get_social_connections(
        self, provider: str, uid: Union[str, Iterable[str]]
    ) -> List[SocialConnection]:
        data = await self.get_social_connections(provider, uid)
        return [SocialConnection(conn=self, data=x) for x in data]

    @promisify
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
        data = await self.get_leaderboard(stat=stat, guild_id=guild_id)
        return leaderboard_class(conn=self, data=data)

    @promisify
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

        queryset = await self.get_trainers(q=nickname)

        if len(queryset) == 1:
            return Trainer(conn=self, data=queryset[0])
        else:
            raise IndexError
