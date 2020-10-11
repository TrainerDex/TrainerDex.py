import datetime
from decimal import Decimal
from uuid import UUID
from typing import Dict, Union

from dateutil.parser import parse

from . import abc
from .http import HTTPClient, UPDATE_KEYS_ENUM_IN
from .utils import con

odt = con(parse)


class Level:
    def __init__(self, level: int, min: int, max: Union[int, float]) -> None:
        self.level = level
        self.min = min
        self.max = max

    def __eq__(self, o) -> bool:
        return self.level == o.level

    def __hash__(self):
        return hash(self.level)

    def __str__(self) -> str:
        return str(self.level)

    def __repr__(self) -> str:
        return f"Level({self.level})"


def get_level(xp: int = None, level: int = None) -> int:
    levels = {
        1: (0, 1000),
        2: (1000, 3000),
        3: (3000, 6000),
        4: (6000, 10000),
        5: (10000, 15000),
        6: (15000, 21000),
        7: (21000, 28000),
        8: (28000, 36000),
        9: (36000, 45000),
        10: (45000, 55000),
        11: (55000, 65000),
        12: (65000, 75000),
        13: (75000, 85000),
        14: (85000, 100000),
        15: (100000, 120000),
        16: (120000, 140000),
        17: (140000, 160000),
        18: (160000, 185000),
        19: (185000, 210000),
        20: (210000, 260000),
        21: (260000, 335000),
        22: (335000, 435000),
        23: (435000, 560000),
        24: (560000, 710000),
        25: (710000, 900000),
        26: (900000, 1100000),
        27: (1100000, 1350000),
        28: (1350000, 1650000),
        29: (1650000, 2000000),
        30: (2000000, 2500000),
        31: (2500000, 3000000),
        32: (3000000, 3750000),
        33: (3750000, 4750000),
        34: (4750000, 6000000),
        35: (6000000, 7500000),
        36: (7500000, 9500000),
        37: (9500000, 12000000),
        38: (12000000, 15000000),
        39: (15000000, 20000000),
        40: (20000000, float("inf")),
    }
    if xp:
        return [Level(k, *v) for k, v in levels.items() if v[0] <= xp < v[1]][0]
    elif level:
        return Level(level, *levels[level])


class BaseUpdate(abc.BaseClass):
    def __init__(self, conn: HTTPClient, data: Dict[str, Union[str, int]], trainer=None) -> None:
        super().__init__(conn, data)
        self._trainer = trainer

    def __eq__(self, o) -> bool:
        return self.uuid == o.uuid

    def __hash__(self):
        return hash(self.uuid)

    @property
    def level(self) -> Level:
        xp = getattr(self, "total_xp", None)
        if xp:
            return get_level(xp=xp)

    async def trainer(self):
        if self._trainer:
            return self._trainer

        # have to import Trainer late to prevent circular imports
        from .trainer import Trainer

        data = await self.http.get_trainer(self._trainer_id)
        self._trainer = Trainer(data=data, conn=self.http)

        return self._trainer


class Update(BaseUpdate):
    def _update(self, data: Dict[str, Union[str, int]]) -> None:
        data = {
            UPDATE_KEYS_ENUM_IN.get(k): v
            for k, v in data.items()
            if (UPDATE_KEYS_ENUM_IN.get(k) is not None)
        }
        self.uuid = UUID(data.get("uuid"))
        self._trainer_id = data.get("trainer")
        self.update_time = odt(data.get("update_time"))
        self.submission_date = odt(data.get("submission_date"))
        self.data_source = data.get("data_source")
        self.total_xp = data.get("total_xp")
        self.pokedex_total_caught = data.get("pokedex_total_caught")
        self.pokedex_total_seen = data.get("pokedex_total_seen")
        self.pokedex_gen1 = data.get("pokedex_gen1")
        self.pokedex_gen2 = data.get("pokedex_gen2")
        self.pokedex_gen3 = data.get("pokedex_gen3")
        self.pokedex_gen4 = data.get("pokedex_gen4")
        self.pokedex_gen5 = data.get("pokedex_gen5")
        self.pokedex_gen6 = data.get("pokedex_gen6")
        self.pokedex_gen7 = data.get("pokedex_gen7")
        self.pokedex_gen8 = data.get("pokedex_gen8")
        self.travel_km = con(Decimal, data.get("travel_km"))
        self.capture_total = data.get("capture_total")
        self.evolved_total = data.get("evolved_total")
        self.hatched_total = data.get("hatched_total")
        self.pokestops_visited = data.get("pokestops_visited")
        self.big_magikarp = data.get("big_magikarp")
        self.battle_attack_won = data.get("battle_attack_won")
        self.battle_training_won = data.get("battle_training_won")
        self.small_rattata = data.get("small_rattata")
        self.pikachu = data.get("pikachu")
        self.unown = data.get("unown")
        self.raid_battle_won = data.get("raid_battle_won")
        self.legendary_battle_won = data.get("legendary_battle_won")
        self.berries_fed = data.get("berries_fed")
        self.hours_defended = data.get("hours_defended")
        self.challenge_quests = data.get("challenge_quests")
        self.max_level_friends = data.get("max_level_friends")
        self.trading = data.get("trading")
        self.trading_distance = data.get("trading_distance")
        self.great_league = data.get("great_league")
        self.ultra_league = data.get("ultra_league")
        self.master_league = data.get("master_league")
        self.photobomb = data.get("photobomb")
        self.pokemon_purified = data.get("pokemon_purified")
        self.rocket_grunts_defeated = data.get("rocket_grunts_defeated")
        self.type_normal = data.get("type_normal")
        self.type_fighting = data.get("type_fighting")
        self.type_flying = data.get("type_flying")
        self.type_poison = data.get("type_poison")
        self.type_ground = data.get("type_ground")
        self.type_rock = data.get("type_rock")
        self.type_bug = data.get("type_bug")
        self.type_ghost = data.get("type_ghost")
        self.type_steel = data.get("type_steel")
        self.type_fire = data.get("type_fire")
        self.type_water = data.get("type_water")
        self.type_grass = data.get("type_grass")
        self.type_electric = data.get("type_electric")
        self.type_psychic = data.get("type_psychic")
        self.type_ice = data.get("type_ice")
        self.type_dragon = data.get("type_dragon")
        self.type_dark = data.get("type_dark")
        self.type_fairy = data.get("type_fairy")
        self.gymbadges_total = data.get("gymbadges_total")
        self.gymbadges_gold = data.get("gymbadges_gold")
        self.stardust = data.get("stardust")

    async def refresh_from_api(self) -> None:
        data = await self.http.get_update(self.uuid)
        self._update(data)

    async def edit(self, **options) -> None:
        """|coro|

        Edits the current trainer

        .. note::
            Changing UUIDs is forever unsupported
        """

        if isinstance(options.get("update_time"), datetime.datetime):
            options["update_time"] = options["update_time"].isoformat()

        if isinstance(options.get("submission_date"), datetime.datetime):
            options["submission_date"] = options["submission_date"].isoformat()

        if isinstance(options.get("travel_km"), (float, Decimal)):
            options["travel_km"] = str(options["travel_km"])

        new_data = await self.http.edit_update(self._trainer_id, self.uuid, **options)
        self._update(new_data)


class PartialUpdate(BaseUpdate):
    def _update(self, data):
        data = {
            UPDATE_KEYS_ENUM_IN.get(k): v
            for k, v in data.items()
            if (UPDATE_KEYS_ENUM_IN.get(k) is not None)
        }
        self.uuid = UUID(data.get("uuid"))
        self._trainer_id = data.get("trainer")
        self.update_time = odt(data.get("update_time"))
        self.total_xp = data.get("total_xp")
        self.unloaded_data = data.get("modified_extra_fields")

    async def upgrade(self) -> Update:
        data = await self.http.get_update(self._trainer_id, self.uuid)
        return Update(self.http, data)
