from typing import Dict, Union


class Faction:
    def __init__(self, i: int) -> None:
        FACTION_DATA = [
            {"id": 0, "verbose_name": "Teamless", "colour": 9605778},
            {"id": 1, "verbose_name": "Mystic", "colour": 1535},
            {"id": 2, "verbose_name": "Valor", "colour": 16711680},
            {"id": 3, "verbose_name": "Instinct", "colour": 16774656},
        ]
        self._update(FACTION_DATA[i])

    def _update(self, data: Dict[str, Union[str, int]]) -> None:
        self.id = int(data.get("id"))
        self.verbose_name = data.get("verbose_name")
        self.colour = data.get("colour")
        self.color = self.colour

    def __str__(self) -> str:
        return self.verbose_name

    def __repr__(self) -> str:
        return f"Faction({self.id})"

    def __eq__(self, o) -> bool:
        return self.id == o.id

    def __hash__(self):
        return hash(self.id)
