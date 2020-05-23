import requests
import json
import datetime
from .trainer import Trainer
from .update import Update
from .cached import DiscordUser
from .http import request_status, api_url
from .user import User
from .leaderboard import DiscordLeaderboard, WorldwideLeaderboard

class Client:
	"""Interact with the TrainerDex API
	
	Supply an api token when calling the class.
	"""
	
	def __init__(self, token=None, identifier=None):
		headers = {'content-type':'application/json'}
		if token!=None:
			headers['authorization'] = 'Token '+token
		self.headers = headers
		if identifier:
			self.identifier = str(identifier)
	
	def get_trainer_from_username(self, username, detail=False):
		"""Returns a Trainer object from a Trainers username"""
		params = {
			'detail': '1' if detail is True else '0',
			'q': username
		}
		r = requests.get(api_url+'trainers/', params=params, headers=self.headers)
		print(request_status(r))
		try:
			r = r.json()[0]
		except IndexError:
			return None
		return Trainer(r) if r else None
	
	def discord_to_users(self, memberlist):
		"""
		expects a list of discord.py user objects
		returns a list of TrainerDex.py user objects
		"""
		_memberlist = self.get_discord_user(x.id for x in memberlist)
		return list(set(x.owner() for x in _memberlist))
	
	def create_trainer(self, username, team, start_date=None, has_cheated=None, last_cheated=None, currently_cheats=None, statistics=True, daily_goal=None, total_goal=None, prefered=True, account=None, verified=False):
		"""Add a trainer to the database"""
		args = locals()
		url = api_url+'trainers/'
		payload = {
			'username': username,
			'faction': team,
			'statistics': statistics,
			'prefered': prefered,
			'last_modified': datetime.datetime.utcnow().isoformat(),
			'owner': account,
			'verified': verified
		}
		
		for i in args:
			if args[i] is not None and i not in ['self', 'username', 'team', 'account', 'start_date']:
				payload[i] = args[i]
			elif args[i] is not None and i=='start_date':
				payload[i] = args[i].date().isoformat()
		
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return Trainer(r.json())
		
	def update_trainer(self, trainer, username=None, start_date=None, has_cheated=None, last_cheated=None, currently_cheats=None, statistics=None, daily_goal=None, total_goal=None, prefered=None):
		"""Update parts of a trainer in a database"""
		args = locals()
		if not isinstance(trainer, Trainer):
			raise ValueError
		url = api_url+'trainers/'+str(trainer.id)+'/'
		payload = {
			'last_modified': datetime.datetime.utcnow().isoformat()
		}
		
		for i in args:
			if args[i] is not None and i not in ['self', 'trainer', 'start_date']:
				payload[i] = args[i]
			elif args[i] is not None and i=='start_date':
				payload[i] = args[i].date().isoformat()
		
		r = requests.patch(url, data=json.dumps(payload), headers=self.headers)
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
		
		if self.identifier:
			payload['meta_source'] = self.identifier
		
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
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
		r = requests.put(url, data=json.dumps(payload), headers=self.headers)
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
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
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
		r = requests.patch(url, data=json.dumps(payload), headers=self.headers)
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
			
		r = requests.get(api_url+'trainers/'+str(id_)+'/', headers=self.headers) if respect_privacy is True else requests.get(api_url+'trainers/'+str(id_)+'/', params=parameters, headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return Trainer(r.json())
	
	def get_detailed_update(self, uid, uuid):
		"""Returns the update object for the ID"""
		
		r = requests.get(api_url+'users/'+str(uid)+'/update/'+str(uuid)+'/', headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return Update(r.json())
	
	def get_user(self, uid):
		"""Returns the User object for the ID"""
		
		r = requests.get(api_url+'users/'+str(uid)+'/', headers=self.headers)
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
		r = requests.get(api_url+'users/social/', params=params, headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		output = r.json()
		result = []
		for x in output:
			result.append(DiscordUser(x))
		return result
	
	def get_all_users(self):
		"""Returns all the users"""
		
		r = requests.get(api_url+'users/', headers=self.headers)
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
		
		r = requests.get(api_url+'leaderboard/discord/'+str(guild)+'/', headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return DiscordLeaderboard(r.json())
	
	
	def get_worldwide_leaderboard(self):
		"""
		Returns: `trainerdex.WorldwideLeaderboard`
		"""
		
		r = requests.get(api_url+'leaderboard/', headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return WorldwideLeaderboard(r.json())
