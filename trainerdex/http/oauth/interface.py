from __future__ import annotations

import os
from abc import abstractmethod

from trainerdex.http.interface import iHTTPClient


class iOAuthClient(iHTTPClient):
    ORIGIN = os.environ.get("TRAINERDEX_ORIGIN", "https://trainerdex.app")

    @abstractmethod()
    def authenticate(self, client_id: str, client_secret: str, *args, **kwargs):
        ...
