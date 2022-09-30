import asyncio
import datetime
import json
import logging
import sys
from decimal import Decimal
from typing import Dict, Iterable, List, Optional, Union
from urllib.parse import quote as _uriquote
from uuid import UUID

import aiohttp
import aiohttp.web

from . import __version__
from .exceptions import Forbidden, HTTPException, NotFound

log: logging.Logger = logging.getLogger(__name__)

# this translates the API v2 field names to API v1 field names
# this is so we can program the rest of the bot as if we're using API v2
UPDATE_KEYS_ENUM_OUT = {
    "uuid": "uuid",
    "trainer": "trainer",
    "update_time": "update_time",
    "submission_date": "submission_date",
    "data_source": "data_source",
    "total_xp": "total_xp",
    "gymbadges_gold": "gymbadges_gold",
    "pokedex_total_caught": "pokedex_caught",
    "pokedex_total_seen": "pokedex_seen",
    "pokedex_gen1": "badge_pokedex_entries",
    "pokedex_gen2": "badge_pokedex_entries_gen2",
    "pokedex_gen3": "badge_pokedex_entries_gen3",
    "pokedex_gen4": "badge_pokedex_entries_gen4",
    "pokedex_gen5": "badge_pokedex_entries_gen5",
    "pokedex_gen6": "badge_pokedex_entries_gen6",
    "pokedex_gen7": "badge_pokedex_entries_gen7",
    "pokedex_gen8": "badge_pokedex_entries_gen8",
    "travel_km": "badge_travel_km",
    "capture_total": "badge_capture_total",
    "evolved_total": "badge_evolved_total",
    "hatched_total": "badge_hatched_total",
    "pokestops_visited": "badge_pokestops_visited",
    "unique_pokestops": "badge_unique_pokestops",
    "big_magikarp": "badge_big_magikarp",
    "battle_attack_won": "badge_battle_attack_won",
    "battle_training_won": "badge_battle_training_won",
    "small_rattata": "badge_small_rattata",
    "pikachu": "badge_pikachu",
    "unown": "badge_unown",
    "raid_battle_won": "badge_raid_battle_won",
    "legendary_battle_won": "badge_legendary_battle_won",
    "berries_fed": "badge_berries_fed",
    "hours_defended": "badge_hours_defended",
    "challenge_quests": "badge_challenge_quests",
    "max_level_friends": "badge_max_level_friends",
    "trading": "badge_trading",
    "trading_distance": "badge_trading_distance",
    "great_league": "badge_great_league",
    "ultra_league": "badge_ultra_league",
    "master_league": "badge_master_league",
    "photobomb": "badge_photobomb",
    "pokemon_purified": "badge_pokemon_purified",
    "rocket_grunts_defeated": "badge_rocket_grunts_defeated",
    "rocket_giovanni_defeated": "badge_rocket_giovanni_defeated",
    "buddy_best": "badge_buddy_best",
    "seven_day_streaks": "badge_7_day_streaks",
    "unique_raid_bosses_defeated": "badge_unique_raid_bosses_defeated",
    "raids_with_friends": "badge_raids_with_friends",
    "pokemon_caught_at_your_lures": "badge_pokemon_caught_at_your_lures",
    "wayfarer": "badge_wayfarer",
    "total_mega_evos": "badge_total_mega_evos",
    "unique_mega_evos": "badge_unique_mega_evos",
    "type_normal": "badge_type_normal",
    "type_fighting": "badge_type_fighting",
    "type_flying": "badge_type_flying",
    "type_poison": "badge_type_poison",
    "type_ground": "badge_type_ground",
    "type_rock": "badge_type_rock",
    "type_bug": "badge_type_bug",
    "type_ghost": "badge_type_ghost",
    "type_steel": "badge_type_steel",
    "type_fire": "badge_type_fire",
    "type_water": "badge_type_water",
    "type_grass": "badge_type_grass",
    "type_electric": "badge_type_electric",
    "type_psychic": "badge_type_psychic",
    "type_ice": "badge_type_ice",
    "type_dragon": "badge_type_dragon",
    "type_dark": "badge_type_dark",
    "type_fairy": "badge_type_fairy",
    "battle_hub_stats_wins": "battle_hub_stats_wins",
    "battle_hub_stats_battles": "battle_hub_stats_battles",
    "battle_hub_stats_stardust": "battle_hub_stats_stardust",
    "battle_hub_stats_streak": "battle_hub_stats_streak",
}
UPDATE_KEYS_ENUM_IN = {v: k for k, v in UPDATE_KEYS_ENUM_OUT.items() if v is not None}
UPDATE_KEYS_READ_ONLY = ("uuid", "trainer", "submission_date")

TRAINER_KEYS_ENUM_OUT = {
    "old_id": "id",
    "id": "owner",
    "nickname": "username",
    "start_date": "start_date",
    "faction": "faction",
    "trainer_code": "trainer_code",
    "is_banned": "currently_cheats",
    "is_verified": "verified",
    "last_modified": "last_modified",
    "is_visible": "statistics",
}
TRAINER_KEYS_ENUM_IN = {
    "id": "old_id",
    "owner": "id",
    "username": "nickname",
    "start_date": "start_date",
    "faction": "faction",
    "trainer_code": "trainer_code",
    "currently_cheats": "is_banned",
    "last_modified": "last_modified",
    "update_set": "updates",
    "verified": "is_verified",
    "statistics": "is_visible",
}
TRAINER_KEYS_READ_ONLY = ("id", "owner", "username", "currently_cheats")


async def json_or_text(response: aiohttp.web.Response) -> Union[Dict, str]:
    text = await response.text(encoding="utf-8")
    if response.headers.get("content-type") == "application/json":
        return json.loads(text)
    return text


class Route:
    BASE = "https://trainerdex.app/api/v1"

    def __init__(self, method: str, path: str, **parameters) -> None:
        self.path = path
        self.method = method
        url = self.BASE + self.path
        if parameters:
            self.url = url.format(
                **{k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()}
            )
        else:
            self.url = url


class HTTPClient:
    """Represents an HTTP client sending HTTP requests to the TrainerDex API."""

    SUCCESS_LOG = "{method} {url} has received {text}"
    REQUEST_LOG = "{method} {url} with {json} has returned {status}"

    def __init__(self, token: str = None, loop=None) -> None:
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.session = aiohttp.ClientSession()
        self.token = token

        user_agent = (
            "TrainerDex.py (https://github.com/TrainerDex/TrainerDex.py {0}) "
            "Python/{1[0]}.{1[1]} "
            "aiohttp/{2}"
        )
        self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)

    async def request(self, route: Route, **kwargs) -> Union[Dict, str]:
        method = route.method
        url = route.url

        headers = {
            "User-Agent": self.user_agent,
        }

        if self.token is not None:
            headers["Authorization"] = "Token " + self.token

        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.dumps(kwargs.pop("json"), ensure_ascii=True)

        kwargs["headers"] = headers

        for tries in range(5):
            try:
                async with self.session.request(method, url, **kwargs) as r:
                    log.info(
                        "{0} {1} with {2} has returned {3}".format(
                            method, url, kwargs.get("data"), r.status
                        )
                    )

                    data = await json_or_text(r)

                    # SUCCESS: Return data
                    if 300 > r.status >= 200:
                        log.debug("{0} {1} has received {2}".format(method, url, data))
                        return data

                    # Error, retry
                    if r.status in {500, 502}:
                        await asyncio.sleep(1 + tries * 2)
                        continue

                    # Error, don't retry
                    if r.status in {401, 403, 423}:
                        raise Forbidden(r, data)
                    elif r.status == 404:
                        raise NotFound(r, data)
                    else:
                        raise HTTPException(r, data)

            # This is handling exceptions from the request
            except OSError as e:
                # Connection reset by peer
                if tries < 4 and e.errno in (54, 10054):
                    continue
                raise

        # We've run out of retries, raise.
        raise HTTPException(r, data)

    # Update management

    def get_update(self, trainer_id: int, update_uuid: Union[str, UUID]) -> Dict:
        r = Route(
            "GET",
            "/trainers/{trainer_id}/updates/{update_uuid}/",
            trainer_id=trainer_id,
            update_uuid=update_uuid,
        )

        return self.request(r)

    def get_updates_for_trainer(self, trainer_id: int) -> Dict:
        r = Route(
            "GET",
            "/trainers/{trainer_id}/updates/",
            trainer_id=trainer_id,
        )

        return self.request(r)

    def create_update(self, trainer_id: int, kwargs) -> Dict:
        r = Route("POST", "/trainers/{trainer_id}/updates/", trainer_id=trainer_id)

        payload = {
            UPDATE_KEYS_ENUM_OUT.get(k): v
            for k, v in kwargs.items()
            if (UPDATE_KEYS_ENUM_OUT.get(k) is not None) and (k != "uuid")
        }

        for k, v in payload.items():
            if isinstance(v, Decimal):
                payload[k] = str(v)
            elif isinstance(v, (datetime.date, datetime.datetime)):
                payload[k] = v.isoformat()

        return self.request(r, json=payload)

    def edit_update(self, trainer_id: int, update_uuid: Union[str, UUID], **kwargs) -> Dict:
        r = Route(
            "PATCH",
            "/trainers/{trainer_id}/updates/{update_uuid}/",
            trainer_id=trainer_id,
            update_uuid=update_uuid,
        )

        payload = {
            UPDATE_KEYS_ENUM_OUT.get(k): v
            for k, v in kwargs.items()
            if (UPDATE_KEYS_ENUM_OUT.get(k) is not None)
            and (UPDATE_KEYS_ENUM_OUT.get(k) not in UPDATE_KEYS_READ_ONLY)
        }
        payload["trainer"] = trainer_id

        for k, v in payload.items():
            if isinstance(v, Decimal):
                payload[k] = str(v)
            elif isinstance(v, (datetime.date, datetime.datetime)):
                payload[k] = v.isoformat()

        return self.request(r, json=payload)

    # Trainer management

    def get_trainer(self, trainer_id: int) -> Dict:
        r = Route("GET", "/trainers/{trainer_id}/", trainer_id=trainer_id)

        return self.request(r)

    def get_trainers(self, **kwargs) -> List[Dict]:
        r = Route("GET", "/trainers/")

        return self.request(r, params=kwargs)

    def create_trainer(self, **kwargs) -> Dict:
        r = Route("POST", "/trainers/")

        payload = {
            TRAINER_KEYS_ENUM_OUT.get(k): v
            for k, v in kwargs.items()
            if (TRAINER_KEYS_ENUM_OUT.get(k) is not None)
            and (TRAINER_KEYS_ENUM_OUT.get(k) != "id")
        }

        for k, v in payload.items():
            if isinstance(v, Decimal):
                payload[k] = str(v)
            elif isinstance(v, (datetime.date, datetime.datetime)):
                payload[k] = v.isoformat()

        return self.request(r, json=payload)

    def edit_trainer(self, trainer_id: int, **kwargs) -> Dict:
        r = Route("PATCH", "/trainers/{trainer_id}/", trainer_id=trainer_id)

        payload = {
            TRAINER_KEYS_ENUM_OUT.get(k): v
            for k, v in kwargs.items()
            if (TRAINER_KEYS_ENUM_OUT.get(k) is not None)
            and (TRAINER_KEYS_ENUM_OUT.get(k) not in TRAINER_KEYS_READ_ONLY)
        }

        for k, v in payload.items():
            if isinstance(v, Decimal):
                payload[k] = str(v)
            elif isinstance(v, (datetime.date, datetime.datetime)):
                payload[k] = v.isoformat()

        return self.request(r, json=payload)

    def get_user(self, user_id: int) -> Dict:
        r = Route("GET", "/users/{user_id}/", user_id=user_id)

        return self.request(r)

    def get_users(self) -> List[Dict]:
        r = Route("GET", "/users/")

        return self.request(r)

    def create_user(self, username: str, first_name: Optional[str] = None) -> Dict:
        r = Route("POST", "/users/")

        payload = {"username": username}

        if first_name:
            payload["first_name"] = first_name

        return self.request(r, json=payload)

    def edit_user(self, user_id, username: str, first_name: Optional[str] = None) -> Dict:
        r = Route("PATCH", "/users/{user_id}/", user_id=user_id)

        payload = {"username": username}

        if first_name:
            payload["first_name"] = first_name

        return self.request(r, json=payload)

    def get_social_connections(self, provider: str, uid: Union[str, Iterable[str]]) -> List[Dict]:
        r = Route("GET", "/users/social/")

        params = {"provider": provider}
        if isinstance(uid, str):
            uid = (uid,)
        params["uid"] = ",".join(uid)

        return self.request(r, params=params)

    def create_social_connection(
        self, user: int, provider: str, uid: str, extra_data: Optional[Dict] = None
    ) -> Dict:
        r = Route("PUT", "/users/social/")

        payload = {"user": user, "provider": provider, "uid": uid}

        if extra_data:
            payload["extra_data"] = extra_data

        return self.request(r, json=payload)

    # Leaderboard requests

    def get_leaderboard(
        self,
        stat: str = None,
        guild_id: Optional[int] = None,
        community: Optional[str] = None,
        country: Optional[str] = None,
    ) -> Dict:
        endpoint = "/leaderboard/"

        if guild_id:
            endpoint += "discord/{}/".format(guild_id)
        elif community:
            endpoint += "community/{}/".format(community)
        elif country:
            endpoint += "country/{}/".format(country)
        else:
            endpoint += "v1.1/"

        if stat:
            endpoint += "{stat}/".format(stat=stat)

        r = Route("GET", endpoint)
        return self.request(r)
