import datetime
import decimal
import json
import re
from typing import Iterable, List, Union

import requests

from trainerdex.trainer import Trainer
from trainerdex.update import Update
from trainerdex.cached import DiscordUser
from trainerdex.http import request_status, api_url
from trainerdex.user import User
from trainerdex.leaderboard import DiscordLeaderboard, WorldwideLeaderboard
from trainerdex.exceptions import *

class Client:
	"""The core class to trainerdex.py.
		
	Attributes
	----------
	token : str, optional
		a token required for writing to the database and some read operations, if blank, many functions will be disabled
	
	Methods
	-------
	search_trainer(nickname)
		Searches the database for a trainer that may currently or previous donned a certain nickname
	discord_to_users(memberlist)
		Convenience method for getting a large number of users at once
	create_trainer(username, faction, start_date, has_cheated, last_cheated, currently_cheats, daily_goal, total_goal, account, verified)
		Still due to change
	update_trainer(trainer, start_date, faction, trainer_code, has_cheated, last_cheated, currently_cheats, daily_goal, total_goal, verified)
		Update parts of a trainer profile
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
		trainerdex.exceptions.MutlipleResultsFound
			Found more than one result, this would be due to an API error and we can't help you.
		trainerdex.exceptions.NoResultsFound
			No... results.. found. Honestly, documenting feels like training a puppy to sh*t on the floor.
		
		"""
		
		url = '{}trainers/'.format(api_url)
		query = {
			'detail': '1',
			'q': nickname
		}
		response = requests.get(url, params=query, headers=self._headers)
		print(request_status(response))
			
		if len(response.json()) == 1:
			return Trainer(response.json()[0])
		elif len(response.json()) > 1:
			raise MutlipleResultsFound
		else:
			raise NoResultsFound
	
	def discord_to_users(self, memberlist: Iterable) -> List[User]:
		"""Convenience function which collects user IDs en mass
		
		Parameters
		----------
		memberlist : iterable
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
				except NoResultsFound:
					pass
			else:
				try:
					users.add(self.get_discord_user(x.id))
				except NoResultsFound:
					pass
				except AttributeError:
					# Not a compatible type, ignore silently
					pass
		
		return list(users)
	
	def create_trainer(
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
		"""Add a trainer to the database
		
		Parameters
		----------
		account : trainerdex.User
			
		faction : int
		start_date : datetime.date, optional
		has_cheated: bool, optional
		last_cheated: datetime.date, optional
		currently_cheats: bool, optional
		daily_goal: int, optional
		total_goal: int, optional
		verified: bool, optional
		
		Returns
		-------
		trainerdex.Trainer
		
		"""
		
		url = '{}trainers/'.format(api_url)
		
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
		"""Update parts of a trainer profile
		
		Parameters
		----------
		trainer : trainerdex.Trainer
		start_date: datetime.date, optional
		faction : int, optional
		trainer_code: str, optional
		has_cheated: bool, optional
		last_cheated: datetime.date, optional
		currently_cheats: bool, optional
		daily_goal: int, optional
		total_goal: int, optional
		verified: bool, optional
		
		Returns
		-------
		trainerdex.Trainer
		
		"""
		# Clone parameters, delete self and anything with None, we don't want that
		parameters = {k:v for k, v in locals().items() if v is not None}
		del parameters['self']
		
		assert type(trainer) == Trainer
		
		url = '{}trainers/{}/'.format(api_url, trainer.id)
		
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
		"""Add a Update object to the database
		
		Parameters
		----------
		
		trainer: int or trainerdex.Trainer
		update_time: datetime.datetime, optional
		total_xp: int, optional
		pokedex_caught: int, optional
		pokedex_seen: int, optional
		gymbadges_total: int, optional
		gymbadges_gold: int, optional
		pokemon_info_stardust: int, optional
		badge_travel_km: Union[decimal.Decimal, float], optional
		badge_pokedex_entries: int, optional
		badge_capture_total: int, optional
		badge_evolved_total: int, optional
		badge_hatched_total: int, optional
		badge_pokestops_visited: int, optional
		badge_big_magikarp: int, optional
		badge_battle_attack_won: int, optional
		badge_battle_training_won: int, optional
		badge_small_rattata: int, optional
		badge_pikachu: int, optional
		badge_unown: int, optional
		badge_pokedex_entries_gen2: int, optional
		badge_raid_battle_won: int, optional
		badge_legendary_battle_won: int, optional
		badge_berries_fed: int, optional
		badge_hours_defended: int, optional
		badge_pokedex_entries_gen3: int, optional
		badge_challenge_quests: int, optional
		badge_max_level_friends: int, optional
		badge_trading: int, optional
		badge_trading_distance: int, optional
		badge_pokedex_entries_gen4: int, optional
		badge_great_league: int, optional
		badge_ultra_league: int, optional
		badge_master_league: int, optional
		badge_photobomb: int, optional
		badge_pokemon_purified: int, optional
		badge_photobombadge_rocket_grunts_defeated: int, optional
		badge_pokedex_entries_gen5: int, optional
		badge_pokedex_entries_gen8: int, optional
		badge_type_normal: int, optional
		badge_type_fighting: int, optional
		badge_type_flying: int, optional
		badge_type_poison: int, optional
		badge_type_ground: int, optional
		badge_type_rock: int, optional
		badge_type_bug: int, optional
		badge_type_ghost: int, optional
		badge_type_steel: int, optional
		badge_type_fire: int, optional
		badge_type_water: int, optional
		badge_type_grass: int, optional
		badge_type_electric: int, optional
		badge_type_psychic: int, optional
		badge_type_ice: int, optional
		badge_type_dragon: int, optional
		badge_type_dark: int, optional
		badge_type_fairy: int, optional
		data_source: str, optional
		"""
		
		parameters = {k:v for k, v in locals().items() if v is not None}
		del parameters['self']
		
		if isinstance(parameters['trainer'], Trainer):
			parameters['trainer'] = parameters['trainer'].id
		
		url = '{}trainers/{}/updates/'.format(api_url, parameters['trainer'])
		
		for key, value in parameters.items():
			if isinstance(value, datetime.date):
				value = value.isoformat()
		
		r = requests.post(url, data=json.dumps(parameters), headers=self._headers)
		print(request_status(r))
		r.raise_for_status()
		return Update(r.json())
		
	def import_discord_user(self, uid, user):
		"""Add a discord user to the database if not already present, get if is present. """
		url = api_url+'users/social/'
		payload = {
			'user': int(user),
			'provider': 'discord',
			'uid': str(uid)
		}
		print(json.dumps(payload))
		r = requests.put(url, data=json.dumps(payload), headers=self._headers)
		print(request_status(r))
		r.raise_for_status()
		return DiscordUser(r.json())
	
	def create_user(self, username, first_name=None, last_name=None):
		"""
		Creates a new user object on database
		Returns the User Object. Must be linked to a new trainer soon after
		"""
		
		url = api_url+'users/'
		payload = {
			'username':username
		}
		if first_name:
			payload['first_name'] = first_name
		if last_name:
			payload['last_name'] = last_name
		r = requests.post(url, data=json.dumps(payload), headers=self._headers)
		print(request_status(r))
		r.raise_for_status()
		return User(r.json())
	
	def update_user(self, user, username=None, first_name=None, last_name=None):
		"""Update user info"""
		
		if not isinstance(user, User):
			raise ValueError
		args = locals()
		url = api_url+'users/'+str(user.id)+'/'
		payload = {}
		for i in args:
			if args[i] is not None and i not in ['self', 'user']:
				payload[i] = args[i]
		r = requests.patch(url, data=json.dumps(payload), headers=self._headers)
		print(request_status(r))
		r.raise_for_status()
		return User(r.json())
	
	def get_trainer(self, id_, respect_privacy=True, detail=True):
		"""Returns the Trainer object for the ID"""
		
		parameters = {}
		if respect_privacy is False:
			parameters['statistics'] = 'force'
		if detail is False:
			parameters['detail'] = 'low'
			
		r = requests.get(api_url+'trainers/'+str(id_)+'/', headers=self._headers) if respect_privacy is True else requests.get(api_url+'trainers/'+str(id_)+'/', params=parameters, headers=self._headers)
		print(request_status(r))
		r.raise_for_status()
		return Trainer(r.json())
	
	def get_detailed_update(self, uid, uuid):
		"""Returns the update object for the ID"""
		
		r = requests.get(api_url+'users/'+str(uid)+'/update/'+str(uuid)+'/', headers=self._headers)
		print(request_status(r))
		r.raise_for_status()
		return Update(r.json())
	
	def get_user(self, uid):
		"""Returns the User object for the ID"""
		
		r = requests.get(api_url+'users/'+str(uid)+'/', headers=self._headers)
		print(request_status(r))
		r.raise_for_status()
		return User(r.json())
	
	def get_discord_user(self, uid=None, user=None, trainer=None):
		"""Returns the DiscordUsers object for the ID
		Expects list of string representions discord IDs, trainer IDs or user IDs
		Returns DiscordUser objects
		"""
		uids = ','.join(uid) if uid else None
		users =','.join(user) if user else None
		trainers = ','.join(trainer) if trainer else None
		params = {
			'provider': 'discord',
			'uid': uids,
			'user': users,
			'trainer': trainers
		}
		r = requests.get(api_url+'users/social/', params=params, headers=self._headers)
		print(request_status(r))
		r.raise_for_status()
		output = r.json()
		result = []
		for x in output:
			result.append(DiscordUser(x))
		return result
	
	def get_all_users(self):
		"""Returns all the users"""
		
		r = requests.get(api_url+'users/', headers=self._headers)
		print(request_status(r))
		r.raise_for_status()
		output = r.json()
		result = []
		for x in output:
			result.append(User(x))
		return result
	
	def get_discord_leaderboard(self, guild):
		"""
		Expects: `int` - Discord Guild ID
		Returns: `trainerdex.DiscordLeaderboard`
		"""
		
		r = requests.get(api_url+'leaderboard/discord/'+str(guild)+'/', headers=self._headers)
		print(request_status(r))
		r.raise_for_status()
		return DiscordLeaderboard(r.json())
	
	
	def get_worldwide_leaderboard(self):
		"""
		Returns: `trainerdex.WorldwideLeaderboard`
		"""
		
		r = requests.get(api_url+'leaderboard/', headers=self._headers)
		print(request_status(r))
		r.raise_for_status()
		return WorldwideLeaderboard(r.json())
