import json
from typing import Dict, Union

from promise import promisify

from trainerdex import abc
from trainerdex.trainer import Trainer
from trainerdex.utils import con


class SocialConnection(abc.BaseClass):
    def _update(self, data: Dict[str, Union[str, int]]) -> None:
        self._user_id = data.get("user")
        self._user = None
        self.provider = data.get("provider")
        self.uid = data.get("uid")
        self.extra_data = con(json.loads, data.get("extra_data"))
        self._trainer_id = data.get("trainer")
        self._trainer = None

    def __eq__(self, o) -> bool:
        return (self.provider, self.uid) == (o.provider, o.uid)

    def __hash__(self):
        return hash((self.provider, self.uid))

    @promisify
    async def user(self):
        if self._user:
            return self._user

        from .user import User

        data = await self.http.get_user(self._user_id)
        self._user = User(data=data, conn=self.http)

        return self._user

    @promisify
    async def trainer(self) -> Trainer:
        if self._trainer:
            return self._trainer

        data = await self.http.get_trainer(self._trainer_id)
        self._trainer = Trainer(data=data, conn=self.http)

        return self._trainer

    @promisify
    async def refresh_from_api(self) -> None:
        data = await self.http.get_social_connections(self.provider, self.uid)
        self._update(data[0])

    def get_discord_user(self, client):
        """Returns discord.User object, if possible

        Parameters
        ----------

            client: Union[:class:`discord.User`, :class:`discord.Bot`, :class:`redbot.core.bot.Red`]

        Returns
        -------

            Optional[:class:`discord.User`]

        """
        if self.provider == "discord":
            try:
                return client.get_user(int(self.uid))
            except:  # noqa: E722
                return None
        raise NotImplementedError

    def get_discord_member(self, ctx, guild=None):
        """Returns discord.Member object, if possible

        Parameters
        ----------

            ctx: Union[:class:`discord.ext.commands.Context`, :class:`redbot.core.commands.context.Context`]
            guild: Optional[:class:`discord.Guild`]

        Returns
        -------

            Optional[:class:`discord.Member`]

        """
        if self.provider == "discord":
            try:
                if ctx:
                    guild = ctx.guild
                return guild.get_member(int(self.uid))
            except:  # noqa: E722
                return None
        raise NotImplementedError
