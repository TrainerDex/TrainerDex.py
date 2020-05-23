import datetime
import json
from typing import Iterable, List, Union
import re.fullmatch

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
	
	def create_trainer(self, username: str, faction: int, start_date: datetime.date = None, has_cheated: bool = None, last_cheated: datetime.date = None, currently_cheats: bool = None, daily_goal: int = None, total_goal: int = None, account: User = None, verified: bool = False) -> Trainer:
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
		
	def update_trainer(self, trainer: Trainer, start_date: datetime.date = None, faction: int = None, trainer_code: str = None, has_cheated: bool = None, last_cheated: datetime.date = None, currently_cheats: bool = None, daily_goal: int = None, total_goal: int = None, verified: bool = None) -> Trainer:
		"""Update parts of a trainer in a database
		
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
	
	def create_update(self, trainer, xp, time_updated=None):
		"""Add a Update object to the database
		
		Arguments:
		trainer - expects a int of trainer's id or a trainer object
		xp
		time_updated - expects datetime.datetime
		
		"""
		
		if isinstance(trainer, Trainer):
			trainer = trainer.id
		url = api_url+'trainers/'+str(trainer)+'/updates/'
		payload = {'trainer' : int(trainer), 'xp' : int(xp)}
		
		if isinstance(time_updated, datetime.datetime):
			payload['update_time'] = time_updated.isoformat()
		elif isinstance(time_updated, type(None)):
			payload['update_time'] = datetime.datetime.utcnow().isoformat()
		else:
			try:
				import maya
			except ModuleNotFoundError:
				pass
			else:
				if isinstance(time_updated, maya.MayaDT):
					payload['update_time'] = time_updated.iso8601()
				else:
					raise
		
		## We're scraping the identifier attribute, please call that each time you need it.
		
		# if self.identifier:
		# 	payload['meta_source'] = self.identifier
		
		r = requests.post(url, data=json.dumps(payload), headers=self._headers)
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
