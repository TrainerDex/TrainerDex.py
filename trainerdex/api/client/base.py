from __future__ import annotations

import datetime
from typing import Iterable, List, Optional, Union

from trainerdex.api.exceptions import NotFound
from trainerdex.api.faction import Faction
from trainerdex.api.http import APIV1Mixin
from trainerdex.api.leaderboard import (
    CommunityLeaderboard,
    CountryLeaderboard,
    GuildLeaderboard,
    Leaderboard,
)
from trainerdex.api.socialconnection import SocialConnection
from trainerdex.api.trainer import Trainer
from trainerdex.api.types.v1.trainer import CreateTrainer
from trainerdex.api.types.v1.user import CreateUser
from trainerdex.api.user import User
from trainerdex.api.utils import HasID


class BaseClient(APIV1Mixin):
    async def get_trainer(self, trainer_id: int) -> Trainer:
        data = await self._v1_get_trainer(trainer_id)
        trainer = Trainer(client=self, data=data)
        await trainer.fetch_updates()
        return trainer

    async def create_trainer(
        self,
        username: str,
        faction: Union[int, Faction],
        start_date: Optional[datetime.date] = None,
        trainer_code: Optional[str] = None,
        verified: bool = True,
        statistics: bool = True,
        user: Optional[User] = None,
    ) -> Trainer:
        """Creates Trainer

        If :parameter:`user` is None, it will create a user. This is the default behavour!
        """
        if user is None:
            user_data = await self._v1_create_user(CreateUser(username=username))
            user = User(client=self, data=user_data)

        assert isinstance(user, User)

        payload = CreateTrainer(
            owner=user.id,
            faction=faction.id if isinstance(faction, Faction) else faction,
            start_date=start_date.isoformat() if isinstance(start_date, datetime.date) else None,
            trainer_code=trainer_code,
            verified=verified,
            statistics=statistics,
        )

        data = await self._v1_create_trainer(payload)
        trainer = Trainer(client=self, data=data)
        user._trainer, trainer._user = trainer, user
        return trainer

    async def get_trainers(
        self, *, team: Union[int, Faction] = None, username: str = None
    ) -> List[Trainer]:
        if isinstance(team, Faction):
            t = team.id
        elif isinstance(team, int):
            assert team in (0, 1, 2, 3)
            t = team
        else:
            t = None

        query = await self._v1_get_trainers(team=t, username=username)
        return [Trainer(client=self, data=trainer) for trainer in query]

    async def get_user(self, user_id: int) -> User:
        data = await self._v1_get_user(user_id)
        return User(client=self, data=data)

    async def get_users(self) -> Iterable[User]:
        data = await self._v1_get_users()
        return tuple(User(client=self, data=d) for d in data)

    async def get_social_connections(
        self, provider: str, uid: Union[str, Iterable[str]]
    ) -> List[SocialConnection]:
        data = await self._v1_get_social_connections(provider=provider, uid=uid)
        return [SocialConnection(client=self, data=x) for x in data]

    async def get_leaderboard(
        self,
        stat: str = "total_xp",
        guild: Union[int, HasID] = None,
        community: Optional[str] = None,
        country: Optional[str] = None,
    ) -> Union[Leaderboard, GuildLeaderboard, CommunityLeaderboard, CountryLeaderboard]:
        if guild is not None:
            if isinstance(guild, HasID):
                guild_id = guild.id
            elif isinstance(guild, int):
                guild_id = guild
            else:
                raise TypeError("guild must be either int or have an int id attribute")
            cls = GuildLeaderboard
        elif community is not None:
            cls = CommunityLeaderboard
        elif country is not None:
            cls = CountryLeaderboard
        else:
            guild_id = None
            cls = Leaderboard

        data = await self._v1_get_leaderboard(
            stat=stat,
            guild_id=guild_id,
            community=community,
            country=country,
        )
        return cls(client=self, data=data)

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

        queryset = await self._v1_get_trainers(q=nickname)

        if len(queryset) == 1:
            return Trainer(client=self, data=queryset[0])
        else:
            raise NotFound(f"Could not find trainer with nickname {nickname}")
