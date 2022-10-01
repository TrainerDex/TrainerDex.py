from __future__ import annotations

import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID as _UUID

from dateutil.parser import parse

from .base import BaseClass
from .utils import convert

if TYPE_CHECKING:
    from .types.v1.update import ReadUpdate

parse_dt = convert(parse)
UUID = convert(_UUID)


class Update(BaseClass):
    def _update(self, data: ReadUpdate) -> None:
        self.uuid = UUID(data["uuid"])
        self.trainer_id = data["trainer"]
        self.update_time = parse_dt(data["update_time"])
        self.total_xp = data["total_xp"]
        self.trainer_level = data["trainer_level"]
        self.pokedex_caught = data["pokedex_caught"]
        self.pokedex_seen = data["pokedex_seen"]
        self.gymbadges_gold = data["gymbadges_gold"]
        self.gym_gold = data["gym_gold"]
        self.travel_km = data["travel_km"]
        self.pokedex_entries = data["pokedex_entries"]
        self.capture_total = data["capture_total"]
        self.evolved_total = data["evolved_total"]
        self.hatched_total = data["hatched_total"]
        self.pokestops_visited = data["pokestops_visited"]
        self.unique_pokestops = data["unique_pokestops"]
        self.big_magikarp = data["big_magikarp"]
        self.battle_attack_won = data["battle_attack_won"]
        self.battle_training_won = data["battle_training_won"]
        self.small_rattata = data["small_rattata"]
        self.pikachu = data["pikachu"]
        self.unown = data["unown"]
        self.pokedex_entries_gen2 = data["pokedex_entries_gen2"]
        self.raid_battle_won = data["raid_battle_won"]
        self.legendary_battle_won = data["legendary_battle_won"]
        self.berries_fed = data["berries_fed"]
        self.hours_defended = data["hours_defended"]
        self.pokedex_entries_gen3 = data["pokedex_entries_gen3"]
        self.challenge_quests = data["challenge_quests"]
        self.max_level_friends = data["max_level_friends"]
        self.trading = data["trading"]
        self.trading_distance = data["trading_distance"]
        self.pokedex_entries_gen4 = data["pokedex_entries_gen4"]
        self.great_league = data["great_league"]
        self.ultra_league = data["ultra_league"]
        self.master_league = data["master_league"]
        self.photobomb = data["photobomb"]
        self.pokedex_entries_gen5 = data["pokedex_entries_gen5"]
        self.pokemon_purified = data["pokemon_purified"]
        self.rocket_grunts_defeated = data["rocket_grunts_defeated"]
        self.rocket_giovanni_defeated = data["rocket_giovanni_defeated"]
        self.buddy_best = data["buddy_best"]
        self.pokedex_entries_gen6 = data["pokedex_entries_gen6"]
        self.pokedex_entries_gen7 = data["pokedex_entries_gen7"]
        self.pokedex_entries_gen8 = data["pokedex_entries_gen8"]
        self.seven_day_streaks = data["seven_day_streaks"]
        self.unique_raid_bosses_defeated = data["unique_raid_bosses_defeated"]
        self.raids_with_friends = data["raids_with_friends"]
        self.pokemon_caught_at_your_lures = data["pokemon_caught_at_your_lures"]
        self.wayfarer = data["wayfarer"]
        self.total_mega_evos = data["total_mega_evos"]
        self.unique_mega_evos = data["unique_mega_evos"]
        self.trainers_referred = data["trainers_referred"]
        self.mvt = data["mvt"]
        self.battle_hub_stats_wins = data["battle_hub_stats_wins"]
        self.battle_hub_stats_battles = data["battle_hub_stats_battles"]
        self.battle_hub_stats_stardust = data["battle_hub_stats_stardust"]
        self.battle_hub_stats_streak = data["battle_hub_stats_streak"]
        self.type_normal = data["type_normal"]
        self.type_fighting = data["type_fighting"]
        self.type_flying = data["type_flying"]
        self.type_poison = data["type_poison"]
        self.type_ground = data["type_ground"]
        self.type_rock = data["type_rock"]
        self.type_bug = data["type_bug"]
        self.type_ghost = data["type_ghost"]
        self.type_steel = data["type_steel"]
        self.type_fire = data["type_fire"]
        self.type_water = data["type_water"]
        self.type_grass = data["type_grass"]
        self.type_electric = data["type_electric"]
        self.type_psychic = data["type_psychic"]
        self.type_ice = data["type_ice"]
        self.type_dragon = data["type_dragon"]
        self.type_dark = data["type_dark"]
        self.type_fairy = data["type_fairy"]
        self.data_source = data["data_source"]

    async def get_trainer(self):
        if getattr(self, "_trainer", None) is None:
            self._trainer = await self.client.get_trainer(self.trainer_id)

        return self._trainer

    async def refresh_from_api(self) -> None:
        data = await self.client._v1_get_update(self.trainer_id, self.uuid)
        self._update(data)

    async def edit(self, **payload) -> None:
        """|coro|

        Edits the current trainer

        .. note::
            Changing UUIDs is forever unsupported
        """

        if isinstance(update_time := payload.get("update_time"), datetime.datetime):
            payload["update_time"] = update_time.isoformat()
        else:
            payload["update_time"] = None

        if (travel_km := payload.get("travel_km")) is not None:
            payload["travel_km"] = str(travel_km)

        new_data = await self.client._v1_edit_update(self.trainer_id, self.uuid, payload)
        self._update(new_data)
