from __future__ import annotations

from typing import TYPE_CHECKING

from trainerdex.api.http.auth.decorators import requires_authentication
from trainerdex.api.http.base import BaseHTTPClient
from trainerdex.api.types.config import ReadDiscordConfig

if TYPE_CHECKING:
    from trainerdex.api.http.base import Response


class ConfigMixin(BaseHTTPClient):
    """Holds the API calls for the Discord Guild Preferences Mixin."""

    @requires_authentication
    def get_all_configs(self) -> Response[list[ReadDiscordConfig]]:
        return self.request("GET", "/api/discord/preferences/")

    @requires_authentication
    def get_config(self, guild_id: int) -> Response[ReadDiscordConfig]:
        return self.request("GET", f"/api/discord/preferences/{guild_id}/")
