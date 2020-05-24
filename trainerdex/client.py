import datetime
import decimal
import json
import re
import uuid
from typing import Iterable, List, Union

import requests

from trainerdex.trainer import Trainer
from trainerdex.update import Update
from trainerdex.cached import DiscordUser
from trainerdex.http import request_status, API_BASE_URL
from trainerdex.user import User
from trainerdex.leaderboard import DiscordLeaderboard, WorldwideLeaderboard
from trainerdex.exceptions import *


class Client:
    """The core class to trainerdex.py.
        
    Attributes
    ----------
    token: str, optional
        a token required for writing to the database and some read operations, if blank, many functions will be disabled
    
    Methods
    -------
    search_trainer(nickname)
        Searches the database for a trainer that may currently or previous donned a certain nickname
    discord_to_users(memberlist)
        Convenience method for getting a large number of users at once
    update_trainer(trainer, start_date, faction, trainer_code, has_cheated, last_cheated, currently_cheats, daily_goal, total_goal, verified)
        Update parts of a trainer profile
    create_update(trainer, update_time, total_xp, data_source, ...)
        Please see help(create_update) for more detail. Lots of optional parameters!
    assign_discord_to_user(uid, user)
        Get or create the assigned connection between the Discord User/Member uid the TrainerDex User
    """
    
    def __init__(self, token: str = None):
        self.token = token
        
        self._headers = {'content-type':'application/json'}
        if self.token:
            self._headers['authorization'] = 'Token {}'.format(self.token)
    
    def search_trainer(self, nickname:str) -> Trainer:
        """Searches the database for a trainer that may currently or previous donned a certain nickname
        
        Parameters
        ----------
        nickname: str
            The nickname of the trainer you want to search for. This search is case insensitive so go wild.
            
        Returns
        -------
        trainerdex.Trainer
            
            
        Raises
        ------
        trainerdex.exceptions.MutlipleResultsFoundError
            Found more than one result, this would be due to an API error and we can't help you.
        trainerdex.exceptions.NoResultsFoundError
            No... results.. found. Honestly, documenting feels like training a puppy to sh*t on the floor.
        
        """
        
        url = '{}trainers/'.format(API_BASE_URL)
        query = {
            'detail': '1',
            'q': nickname,
        }
        response = requests.get(url, params=query, headers=self._headers)
        print(request_status(response))
            
        if len(response.json()) == 1:
            return Trainer(response.json()[0])
        elif len(response.json()) > 1:
            raise MutlipleResultsFoundError
        else:
            raise NoResultsFoundError
    
    def discord_to_users(self, memberlist: Iterable) -> List[User]:
        """Convenience function which collects user IDs en mass
        
        Parameters
        ----------
        memberlist: iterable
            Expects an iterable of int or discord.Member compatible objects, where the int would represent the a Discord Members UID
        
        Returns
        -------
        list
            a list of trainerdex.User objects
        """
        
        users = ()
        
        for x in memberlist:
            if isinstance(x, int):
                try:
                    users.add(self.get_discord_user(x))
                except NoResultsFoundError:
                    pass
            else:
                try:
                    users.add(self.get_discord_user(x.id))
                except NoResultsFoundError:
                    pass
                except AttributeError:
                    # Not a compatible type, ignore silently
                    pass
        
        return list(users)
    
    def _get_user(self, uid: int):
        """Returns the User object for the ID"""
        
        url = '{}users/{}'.format(API_BASE_URL, uid)
        
        r = requests.get(url, headers=self._headers)
        print(request_status(r))
        r.raise_for_status()
        return User(r.json())
    
    def _create_user(self, username: str, first_name: str = None, last_name: str = None) -> User:
        """Creates a new user object on database
        
        Must have consent to run this. Consent is assumed gathered from the user with the API key.
        """
        
        url = '{}users/'.format(API_BASE_URL)
        
        # Clone parameters, delete self, we don't want that
        parameters = locals().copy()
        del parameters['self']
        
        r = requests.post(url, data=json.dumps(payload), headers=self._headers)
        print(request_status(r))
        r.raise_for_status()
        return User(r.json())
    
    def _patch_user(self, user: Union[int, User], first_name: str = None, last_name: str = None) -> User:
        """Patch user info
        
        Due to the nature of how usernames now work in the database, there still isn't an API to reliably update them.
        """
        
        if isinstance(user, User):
            user = user.id
        
        url = '{}users/{}'.format(API_BASE_URL, user)
        
        # Clone parameters, delete self, we don't want that
        parameters = {k:v for k, v in locals().items() if v is not None}
        del parameters['self']
        
        r = requests.patch(url, data=json.dumps(parameters), headers=self._headers)
        print(request_status(r))
        r.raise_for_status()
        return User(r.json())
    
    def get_trainer(self, uid: int) -> Trainer:
        """Returns the Trainer object for the ID"""
        
        url = '{}trainer/{}/'.format(API_BASE_URL, uid)
            
        r = requests.get(url, headers=self._headers)
        print(request_status(r))
        r.raise_for_status()
        return Trainer(r.json())
    
    def _create_trainer(
        self,
        username: str,
        faction: int,
        start_date: datetime.date = None,
        has_cheated: bool = None,
        last_cheated: datetime.date = None,
        currently_cheats: bool = None,
        daily_goal: int = None,
        total_goal: int = None,
        account: User = None,
        verified: bool = False
        ) -> Trainer:
        """Add a trainer to the database"""
        
        url = '{}trainers/'.format(API_BASE_URL)
        
        # Clone parameters, delete self, we don't want that
        parameters = locals().copy()
        del parameters['self']
        
        parameters['last_modified'] = datetime.datetime.utcnow().isoformat()
        
        for key, value in parameters.items():
            if isinstance(value, datetime.date):
                value = value.isoformat()
        
        response = requests.post(url, data=json.dumps(parameters), headers=self._headers)
        print(request_status(response))
        
        r.raise_for_status()
        
        return Trainer(response.json())
        
    def update_trainer(
        self,
        trainer: Trainer,
        start_date: datetime.date = None,
        faction: int = None,
        trainer_code: str = None,
        has_cheated: bool = None,
        last_cheated: datetime.date = None,
        currently_cheats: bool = None,
        daily_goal: int = None,
        total_goal: int = None,
        verified: bool = None
        ) -> Trainer:
        """Update parts of a trainer profile"""
        # Clone parameters, delete self and anything with None, we don't want that
        parameters = {k:v for k, v in locals().items() if v is not None}
        del parameters['self']
        
        assert type(trainer) == Trainer
        
        url = '{}trainers/{}/'.format(API_BASE_URL, trainer.id)
        
        parameters['last_modified'] = datetime.datetime.utcnow().isoformat()
        
        for key, value in parameters.items():
            if isinstance(value, datetime.date):
                value = value.isoformat()
        
        if isinstance(parameters['trainer_code'], str) == True and re.fullmatch(r'((?:\d{4}\s?){3})', parameters['trainer_code']) == False:
            del parameters['trainer_code']
        
        r = requests.patch(url, data=json.dumps(payload), headers=self._headers)
        print(request_status(r))
        r.raise_for_status()
        return Trainer(r.json())
    
    def get_update(self, trainer: Union[int, Trainer], uuid: Union[str, uuid.UUID]):
        """Returns the update object for the ID"""
        
        if isinstance(trainer, Trainer):
            trainer = trainer.id
        
        if isinstance(uuid, uuid.UUID):
            uuid = uuid.hex
        
        url = '{}trainers/{}/updates/{}/'.format(API_BASE_URL, trainer, uuid)
        r = requests.get(url, headers=self._headers)
        print(request_status(r))
        r.raise_for_status()
        return Update(r.json())
    
    def create_update(
        self,
        trainer: Union[int,Trainer],
        update_time: datetime.datetime = None,
        total_xp: int = None,
        pokedex_caught: int = None,
        pokedex_seen: int = None,
        gymbadges_total: int = None,
        gymbadges_gold: int = None,
        pokemon_info_stardust: int = None,
        badge_travel_km: Union[decimal.Decimal, float] = None,
        badge_pokedex_entries: int = None,
        badge_capture_total: int = None,
        badge_evolved_total: int = None,
        badge_hatched_total: int = None,
        badge_pokestops_visited: int = None,
        badge_big_magikarp: int = None,
        badge_battle_attack_won: int = None,
        badge_battle_training_won: int = None,
        badge_small_rattata: int = None,
        badge_pikachu: int = None,
        badge_unown: int = None,
        badge_pokedex_entries_gen2: int = None,
        badge_raid_battle_won: int = None,
        badge_legendary_battle_won: int = None,
        badge_berries_fed: int = None,
        badge_hours_defended: int = None,
        badge_pokedex_entries_gen3: int = None,
        badge_challenge_quests: int = None,
        badge_max_level_friends: int = None,
        badge_trading: int = None,
        badge_trading_distance: int = None,
        badge_pokedex_entries_gen4: int = None,
        badge_great_league: int = None,
        badge_ultra_league: int = None,
        badge_master_league: int = None,
        badge_photobomb: int = None,
        badge_pokemon_purified: int = None,
        badge_photobombadge_rocket_grunts_defeated: int = None,
        badge_pokedex_entries_gen5: int = None,
        badge_pokedex_entries_gen8: int = None,
        badge_type_normal: int = None,
        badge_type_fighting: int = None,
        badge_type_flying: int = None,
        badge_type_poison: int = None,
        badge_type_ground: int = None,
        badge_type_rock: int = None,
        badge_type_bug: int = None,
        badge_type_ghost: int = None,
        badge_type_steel: int = None,
        badge_type_fire: int = None,
        badge_type_water: int = None,
        badge_type_grass: int = None,
        badge_type_electric: int = None,
        badge_type_psychic: int = None,
        badge_type_ice: int = None,
        badge_type_dragon: int = None,
        badge_type_dark: int = None,
        badge_type_fairy: int = None,
        data_source: str = '?',
        ) -> Update:
        """Add a Update object to the database"""
        
        parameters = {k:v for k, v in locals().items() if v is not None}
        del parameters['self']
        
        if isinstance(parameters['trainer'], Trainer):
            parameters['trainer'] = parameters['trainer'].id
        
        url = '{}trainers/{}/updates/'.format(API_BASE_URL, parameters['trainer'])
        
        for key, value in parameters.items():
            if isinstance(value, datetime.date):
                value = value.isoformat()
        
        r = requests.post(url, data=json.dumps(parameters), headers=self._headers)
        print(request_status(r))
        r.raise_for_status()
        return Update(r.json())
        
    def assign_discord_to_user(self, uid: Union[int,str], user: Union[int, User, Trainer]) -> DiscordUser:
        """Get or create the assigned connection between the Discord User/Member uid the TrainerDex User"""
        
        url = '{}users/social/'.format(API_BASE_URL)
        
        parameters = {'provider': 'discord'}
        parameters['uid'] = str(uid)
        if isinstance(user, User):
            parameters['user'] = user.id
        elif isinstance(user, Trainer):
            parameters['user'] = user._get['owner']
        else:
            parameters['user'] = user
        
        r = requests.put(url, data=json.dumps(parameters), headers=self._headers)
        print(request_status(r))
        r.raise_for_status()
        return DiscordUser(r.json())
    
    def get_discord_users(self, users: Union[str, int, User, Trainer, List[Union[str, int, User, Trainer]]]) -> List[DiscordUser]:
        """Retrieves information about Discord connections in the database
        
        Parameters
        ----------
        users: list, int, str, trainerdex.User, trainerdex.Trainer
            Expects either a single or list of any of the types mentioned above, if the type is str or int, it assumes you want to grab the Discord user with that Discord UID
        
        Returns
        -------
        list of trainerdex.DiscordUser, may be empty
        """
        
        url = '{}users/social/'.format(API_BASE_URL)
        
        if not isinstance(users, list):
            users = [users]
        
        parameters = {
            'provider': 'discord',
            'uid': ','.join(str(d) for d in users if type(d) in (int, str)),  # If string or int, assume discord ID
            'user': ','.join(u.id for u in users if type(u) == User),
            'trainer': ','.join(t.id for t in users if type(t) == Trainer),
        }
        r = requests.get(url, params=parameters, headers=self._headers)
        print(request_status(r))
        r.raise_for_status()
        return [DiscordUser(x) for x in r.json()]
    
    def get_discord_leaderboard(self, guild):
        """
        Expects: `int` - Discord Guild ID
        Returns: `trainerdex.DiscordLeaderboard`
        """
        
        r = requests.get(API_BASE_URL+'leaderboard/discord/'+str(guild)+'/', headers=self._headers)
        print(request_status(r))
        r.raise_for_status()
        return DiscordLeaderboard(r.json())
    
    
    def get_worldwide_leaderboard(self):
        """
        Returns: `trainerdex.WorldwideLeaderboard`
        """
        
        r = requests.get(API_BASE_URL+'leaderboard/', headers=self._headers)
        print(request_status(r))
        r.raise_for_status()
        return WorldwideLeaderboard(r.json())
