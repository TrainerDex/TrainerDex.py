from __future__ import annotations

import datetime
from decimal import Decimal as _Decimal
from typing import TYPE_CHECKING
from uuid import UUID as _UUID

from dateutil.parser import parse

from trainerdex.api.base import BaseClass
from trainerdex.api.utils import convert

if TYPE_CHECKING:
    from trainerdex.api.types.v1.update import ReadUpdate

parse_dt = convert(parse)
UUID = convert(_UUID)
Decimal = convert(_Decimal)


class Update(BaseClass):
    def _update(self, data: ReadUpdate) -> None:
        self.uuid = UUID(data["uuid"])
        self.trainer_id = data["trainer"]
        self.update_time = parse_dt(data["update_time"])
        self.total_xp = data.get("total_xp")
        self.trainer_level = data.get("trainer_level")
        self.pokedex_caught = data.get("pokedex_caught")
        self.pokedex_seen = data.get("pokedex_seen")
        self.gymbadges_gold = data.get("gymbadges_gold")
        self.gym_gold = data.get("gym_gold")
        self.travel_km = Decimal(data.get("travel_km"))
        self.pokedex_entries = data.get("pokedex_entries")
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
        self.pokedex_entries_gen2 = data.get("pokedex_entries_gen2")
        self.raid_battle_won = data.get("raid_battle_won")
        self.legendary_battle_won = data.get("legendary_battle_won")
        self.berries_fed = data.get("berries_fed")
        self.hours_defended = data.get("hours_defended")
        self.pokedex_entries_gen3 = data.get("pokedex_entries_gen3")
        self.challenge_quests = data.get("challenge_quests")
        self.max_level_friends = data.get("max_level_friends")
        self.trading = data.get("trading")
        self.trading_distance = data.get("trading_distance")
        self.pokedex_entries_gen4 = data.get("pokedex_entries_gen4")
        self.great_league = data.get("great_league")
        self.ultra_league = data.get("ultra_league")
        self.master_league = data.get("master_league")
        self.photobomb = data.get("photobomb")
        self.pokedex_entries_gen5 = data.get("pokedex_entries_gen5")
        self.pokemon_purified = data.get("pokemon_purified")
        self.rocket_grunts_defeated = data.get("rocket_grunts_defeated")
        self.rocket_giovanni_defeated = data.get("rocket_giovanni_defeated")
        self.buddy_best = data.get("buddy_best")
        self.pokedex_entries_gen6 = data.get("pokedex_entries_gen6")
        self.pokedex_entries_gen7 = data.get("pokedex_entries_gen7")
        self.pokedex_entries_gen8 = data.get("pokedex_entries_gen8")
        self.seven_day_streaks = data.get("seven_day_streaks")
        self.unique_raid_bosses_defeated = data.get("unique_raid_bosses_defeated")
        self.raids_with_friends = data.get("raids_with_friends")
        self.pokemon_caught_at_your_lures = data.get("pokemon_caught_at_your_lures")
        self.wayfarer = data.get("wayfarer")
        self.total_mega_evos = data.get("total_mega_evos")
        self.unique_mega_evos = data.get("unique_mega_evos")
        self.trainers_referred = data.get("trainers_referred")
        self.mvt = data.get("mvt")
        self.battle_hub_stats_wins = data.get("battle_hub_stats_wins")
        self.battle_hub_stats_battles = data.get("battle_hub_stats_battles")
        self.battle_hub_stats_stardust = data.get("battle_hub_stats_stardust")
        self.battle_hub_stats_streak = data.get("battle_hub_stats_streak")
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
