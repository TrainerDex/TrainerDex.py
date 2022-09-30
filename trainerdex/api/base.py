from abc import abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client


class BaseClass:
    def __init__(self, client: Client, data: Any) -> None:
        self.client = client
        self._update(data)

    @abstractmethod
    def _update(self, data: Any) -> None:
        ...
    
    @abstractmethod
    async def refresh_from_api(self) -> None:
        ...
