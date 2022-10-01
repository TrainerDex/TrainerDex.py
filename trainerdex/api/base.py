from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any
from uuid import UUID

if TYPE_CHECKING:
    from trainerdex.api.client import BaseClient


class BaseClass:
    uuid: UUID

    def __init__(self, client: BaseClient, data: Any) -> None:
        self.client = client
        self._update(data)

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.uuid == other.uuid
        else:
            raise TypeError(f"Cannot compare {self.__class__} with other types")

    def __hash__(self):
        return hash(self.uuid)

    @abstractmethod
    def _update(self, data: Any) -> None:
        ...

    @abstractmethod
    async def refresh_from_api(self) -> None:
        ...
