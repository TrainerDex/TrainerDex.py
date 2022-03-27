import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Union
from uuid import UUID

from dateutil.parser import parse

from . import abc
from .http import UPDATE_KEYS_ENUM_IN, HTTPClient
from .utils import con

odt = con(parse)


class Level:
    def __init__(
        self,
        level: int,
        total_xp: int,
        xp_required: Optional[int] = None,
        quest_requirements: Optional[List[Dict[str, str]]] = None,
    ) -> None:
        self.level = level
        self.total_xp = total_xp
        self.xp_required = xp_required
        self.quest_requirements = quest_requirements

    def requirements_to_reach(self) -> Dict[str, Union[int, Dict[str, str]]]:
        return {"total_xp": self.total_xp, "quests": self.quest_requirements}

    @property
    def needs_quests(self) -> bool:
        return self.quest_requirements is not None

    def __eq__(self, o) -> bool:
        return self.level == o.level

    def __hash__(self):
        return hash(self.level)

    def __str__(self) -> str:
        return str(self.level)

    def id(self) -> int:
        return self.level


LEVELS: List[Level] = [
    Level(level=1, total_xp=0, xp_required=1000),
    Level(level=2, total_xp=1000, xp_required=2000),
    Level(level=3, total_xp=3000, xp_required=3000),
    Level(level=4, total_xp=6000, xp_required=4000),
    Level(level=5, total_xp=10_000, xp_required=5000),
    Level(level=6, total_xp=15_000, xp_required=6000),
    Level(level=7, total_xp=21_000, xp_required=7000),
    Level(level=8, total_xp=28_000, xp_required=8000),
    Level(level=9, total_xp=36_000, xp_required=9000),
    Level(level=10, total_xp=45_000, xp_required=10_000),
    Level(level=11, total_xp=55_000, xp_required=10_000),
    Level(level=12, total_xp=65_000, xp_required=10_000),
    Level(level=13, total_xp=75_000, xp_required=10_000),
    Level(level=14, total_xp=85_000, xp_required=15_000),
    Level(level=15, total_xp=100_000, xp_required=20_000),
    Level(level=16, total_xp=120_000, xp_required=20_000),
    Level(level=17, total_xp=140_000, xp_required=20_000),
    Level(level=18, total_xp=160_000, xp_required=25_000),
    Level(level=19, total_xp=185_000, xp_required=25_000),
    Level(level=20, total_xp=210_000, xp_required=50_000),
    Level(level=21, total_xp=260_000, xp_required=75_000),
    Level(level=22, total_xp=335_000, xp_required=100_000),
    Level(level=23, total_xp=435_000, xp_required=125_000),
    Level(level=24, total_xp=560_000, xp_required=150_000),
    Level(level=25, total_xp=710_000, xp_required=190_000),
    Level(level=26, total_xp=900_000, xp_required=200_000),
    Level(level=27, total_xp=1_100_000, xp_required=250_000),
    Level(level=28, total_xp=1_350_000, xp_required=300_000),
    Level(level=29, total_xp=1_650_000, xp_required=350_000),
    Level(level=30, total_xp=2_000_000, xp_required=500_000),
    Level(level=31, total_xp=2_500_000, xp_required=500_000),
    Level(level=32, total_xp=3_000_000, xp_required=750_000),
    Level(level=33, total_xp=3_750_000, xp_required=1_000_000),
    Level(level=34, total_xp=4_750_000, xp_required=1_250_000),
    Level(level=35, total_xp=6_000_000, xp_required=1_500_000),
    Level(level=36, total_xp=7_500_000, xp_required=2_000_000),
    Level(level=37, total_xp=9_500_000, xp_required=2_500_000),
    Level(level=38, total_xp=12_000_000, xp_required=3_000_000),
    Level(level=39, total_xp=15_000_000, xp_required=5_000_000),
    Level(level=40, total_xp=20_000_000, xp_required=6_000_000),
    Level(level=41, total_xp=26_000_000, xp_required=7_500_000),
    Level(level=42, total_xp=33_500_000, xp_required=9_000_000),
    Level(level=43, total_xp=42_500_000, xp_required=11_000_000),
    Level(level=44, total_xp=53_500_000, xp_required=13_000_000),
    Level(level=45, total_xp=66_500_000, xp_required=15_500_000),
    Level(level=46, total_xp=82_000_000, xp_required=18_000_000),
    Level(level=47, total_xp=100_000_000, xp_required=21_000_000),
    Level(level=48, total_xp=121_000_000, xp_required=25_000_000),
    Level(level=49, total_xp=146_000_000, xp_required=30_000_000),
    Level(level=50, total_xp=176_000_000, xp_required=None),
]


def get_possible_levels_from_total_xp(xp: int) -> List[Level]:
    if xp < LEVELS[40].total_xp:
        possible_levels = [
            x
            for x in filter(
                lambda x: x.total_xp <= xp
                and (x.total_xp + x.xp_required > xp if x.xp_required else True),
                LEVELS,
            )
        ]
    else:
        possible_levels = [
            x
            for x in filter(
                lambda x: 20_000_000 <= x.total_xp <= xp,
                LEVELS,
            )
        ]

    return possible_levels


def get_level(level: int) -> Level:
    if level <= len(LEVELS):
        return LEVELS[level - 1]
    else:
        raise ValueError


class BaseUpdate(abc.BaseClass):
    def __init__(self, conn: HTTPClient, data: Dict[str, Union[str, int]], trainer=None) -> None:
        super().__init__(conn, data)
        self._trainer = trainer

    def __eq__(self, o) -> bool:
        return self.uuid == o.uuid

    def __hash__(self):
        return hash(self.uuid)

    @property
    def level(self) -> str:
        if self.total_xp:
            possible_levels = [
                x.level for x in get_possible_levels_from_total_xp(xp=self.total_xp)
            ]
            if min(possible_levels) == max(possible_levels):
                return str(min(possible_levels))
            else:
                return f"{min(possible_levels)}-{max(possible_levels)}"

    async def trainer(self):
        if self._trainer:
            return self._trainer

        # have to import Trainer late to prevent circular imports
        from .trainer import Trainer

        data = await self.http.get_trainer(self._trainer_id)
        self._trainer = Trainer(data=data, conn=self.http)
        await self._trainer.fetch_updates()

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
        self.gymbadges_gold = data.get("gymbadges_gold")

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
        self.unique_pokestops = data.get("unique_pokestops")
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
        self.buddy_best = data.get("buddy_best")
        self.seven_day_streaks = data.get("seven_day_streaks")
        self.unique_raid_bosses_defeated = data.get("unique_raid_bosses_defeated")
        self.raids_with_friends = data.get("raids_with_friends")
        self.pokemon_caught_at_your_lures = data.get("pokemon_caught_at_your_lures")
        self.wayfarer = data.get("wayfarer")
        self.total_mega_evos = data.get("total_mega_evos")
        self.unique_mega_evos = data.get("unique_mega_evos")

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

        self.battle_hub_stats_wins = data.get("battle_hub_stats_wins")
        self.battle_hub_stats_battles = data.get("battle_hub_stats_battles")
        self.battle_hub_stats_stardust = data.get("battle_hub_stats_stardust")
        self.battle_hub_stats_streak = data.get("battle_hub_stats_streak")

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
