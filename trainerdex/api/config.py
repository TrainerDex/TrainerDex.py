from __future__ import annotations

from typing import Any

from trainerdex.api.base import BaseClass
from trainerdex.api.types.config import ReadDiscordConfig


class AsyncManagedProperty:
    def __init__(self, parent: Any, name: str):
        self._parent = parent
        self.__name__ = name

    def get(self) -> Any:
        return getattr(self._parent, f"_{self.__name__}")

    async def set(self, value):
        await self._set_value(value)
        setattr(self._parent, f"_{self.__name__}", value)

    async def _set_value(self, value):
        await self._parent.client.patch_config(self._parent.id, {self.__name__: value})

    def __call__(self, *args, **kwargs) -> Any:
        return self.get()

    def __repr__(self) -> str:
        return f"AsyncManagedProperty({self._parent!r}, {self.__name__!r}) == {self.get()!r}"


class DiscordConfig(BaseClass):
    def _update(self, data: ReadDiscordConfig) -> None:
        self._id: int = data.pop("id")  # type: ignore
        self.managed_properties = set()
        for key, value in data.items():
            setattr(self, f"_{key}", value)
            self.managed_properties.add(key)

    def __getattr__(self, name: str) -> Any:
        if name in self.managed_properties:
            return AsyncManagedProperty(self, name)
        return getattr(self, name)

    @property
    def id(self) -> int:
        return self._id
