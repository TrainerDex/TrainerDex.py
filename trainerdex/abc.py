from typing import Dict, Union

from promise import promisify

from trainerdex.http import HTTPClient


class BaseClass:
    def __init__(self, conn: HTTPClient, data: Dict[str, Union[str, int]]) -> None:
        self.http = conn
        self._update(data)

    def _update(self, data: Dict[str, Union[str, int]]) -> None:
        raise NotImplementedError

    @promisify
    async def refresh_from_api(self) -> None:
        raise NotImplementedError
