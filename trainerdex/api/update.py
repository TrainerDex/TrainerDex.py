import datetime
from decimal import Decimal
from typing import Dict, NamedTuple, Optional, Union
from uuid import UUID

from dateutil.parser import parse

from .base import BaseClass
from .http import HTTPClient
from .utils import convert

odt = convert(parse)


class BaseUpdate(BaseClass):
    def __init__(self, conn: HTTPClient, data: Dict[str, Union[str, int]], trainer=None) -> None:
        super().__init__(conn, data)
        self._trainer = trainer

    def __eq__(self, o) -> bool:
        return self.uuid == o.uuid

    def __hash__(self):
        return hash(self.uuid)

    async def trainer(self):
        if self._trainer:
            return self._trainer

        # have to import Trainer late to prevent circular imports
        from .trainer import Trainer

        data = await self.client.get_trainer(self._trainer_id)
        self._trainer = Trainer(data=data, conn=self.client)
        await self._trainer.fetch_updates()

        return self._trainer


class Update(NamedTuple):
    uuid: UUID
    trainer: int
    update_time: str
    xp: Optional[int]
    total_xp: Optional[int]
    trainer_level: Optional[int]
    total_xp: Optional[int]
    trainer_level: Optional[int]
    pokedex_caught: Optional[int]
    pokedex_seen: Optional[int]
    gymbadges_gold: Optional[int]
    gym_gold: Optional[int]
    travel_km: Optional[str]
    pokedex_entries: Optional[int]
    capture_total: Optional[int]
    evolved_total: Optional[int]
    hatched_total: Optional[int]
    pokestops_visited: Optional[int]
    unique_pokestops: Optional[int]
    big_magikarp: Optional[int]
    battle_attack_won: Optional[int]
    battle_training_won: Optional[int]
    small_rattata: Optional[int]
    pikachu: Optional[int]
    unown: Optional[int]
    pokedex_entries_gen2: Optional[int]
    raid_battle_won: Optional[int]
    legendary_battle_won: Optional[int]
    berries_fed: Optional[int]
    hours_defended: Optional[int]
    pokedex_entries_gen3: Optional[int]
    challenge_quests: Optional[int]
    max_level_friends: Optional[int]
    trading: Optional[int]
    trading_distance: Optional[int]
    pokedex_entries_gen4: Optional[int]
    great_league: Optional[int]
    ultra_league: Optional[int]
    master_league: Optional[int]
    photobomb: Optional[int]
    pokedex_entries_gen5: Optional[int]
    pokemon_purified: Optional[int]
    rocket_grunts_defeated: Optional[int]
    rocket_giovanni_defeated: Optional[int]
    buddy_best: Optional[int]
    pokedex_entries_gen6: Optional[int]
    pokedex_entries_gen7: Optional[int]
    pokedex_entries_gen8: Optional[int]
    seven_day_streaks: Optional[int]
    unique_raid_bosses_defeated: Optional[int]
    raids_with_friends: Optional[int]
    pokemon_caught_at_your_lures: Optional[int]
    wayfarer: Optional[int]
    total_mega_evos: Optional[int]
    unique_mega_evos: Optional[int]
    trainers_referred: Optional[int]
    mvt: Optional[int]
    battle_hub_stats_wins: Optional[int]
    battle_hub_stats_battles: Optional[int]
    battle_hub_stats_stardust: Optional[int]
    battle_hub_stats_streak: Optional[int]
    type_normal: Optional[int]
    type_fighting: Optional[int]
    type_flying: Optional[int]
    type_poison: Optional[int]
    type_ground: Optional[int]
    type_rock: Optional[int]
    type_bug: Optional[int]
    type_ghost: Optional[int]
    type_steel: Optional[int]
    type_fire: Optional[int]
    type_water: Optional[int]
    type_grass: Optional[int]
    type_electric: Optional[int]
    type_psychic: Optional[int]
    type_ice: Optional[int]
    type_dragon: Optional[int]
    type_dark: Optional[int]
    type_fairy: Optional[int]
    data_source: str

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
