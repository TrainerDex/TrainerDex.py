# -*- coding: utf-8 -*-
import requests
import json
import datetime
import maya
from .utils import Team
from .trainer import Trainer
from .update import Update
from .cached import DiscordUser, DiscordServer
from .http import request_status, api_url
from .user import User

class Client:
	"""Interact with the TrainerDex API
	
	Supply an api token when calling the class.
	"""
	
	def __init__(self, token=None):
		headers = {'content-type':'application/json'}
		if token!=None:
			headers['authorization'] = 'Token '+token
		self.headers = headers
	
	@classmethod
	def get_trainer_from_username(self, username, respect_privacy=True):
		"""Returns a Trainer object from a Trainers username"""
		r = requests.get(api_url+'trainers/')
		print(request_status(r))
		r = r.json()
		for i in r:
			if i['username'].lower()==username.lower():
				return Trainer(i, respect_privacy=respect_privacy)
		raise LookupError('Unable to find {} in the database.'.format(username))
	
	@classmethod
	def get_teams(self):
		"""Returns a list of teams, as these are unlikely to change, it's best to just cache the result in the end.
		
		0 - Uncontested
		1 - Mystic
		2 - Valor
		3 - Instinct
		"""
		
		r = requests.get(api_url+'factions/')
		print(request_status(r))
		r.raise_for_status()
		r = r.json()
		
		teams = []
		for i in r:
			teams.append(Team(i))
		return teams
	
	@classmethod
	def get_team(self, id_):
		"""Returns a specific Team object.
		
		0 - Uncontested
		1 - Mystic
		2 - Valor
		3 - Instinct
		"""
		
		r = requests.get(api_url+'factions/'+str(id_)+'/')
		print(request_status(r))
		r.raise_for_status()
		r = r.json()
		return Team(r)
	
	def get_users(self, memberlist):
		member_list = set(x.id for x in memberlist)
		discord_user_list = self.get_all_discord_users()
		filtered_user_list = [x.owner_id for x in discord_user_list if x.id in member_list]
		user_list = self.get_all_users()
		final_user_list = []
		for user in user_list:
			if user.id in filtered_user_list:
				final_user_list.append(user)
		return set(final_user_list)
	
	def create_trainer(self, username, team, start_date=None, has_cheated=None, last_cheated=None, currently_cheats=None, statistics=True, daily_goal=None, total_goal=None, prefered=True, account=None):
		"""Add a trainer to the database"""
		args = locals()
		url = api_url+'trainers/'
		payload = {
			'username': username,
			'faction': team,
			'statistics': statistics,
			'prefered': prefered,
			'last_modified': maya.now().iso8601(),
			'account': account
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
		
	def update_trainer(self, trainer, username=None, start_date=None, has_cheated=None, last_cheated=None, currently_cheats=None, statistics=None, daily_goal=None, total_goal=None, prefered=None, account=None):
		"""Update parts of a trainer in a database"""
		args = locals()
		url = api_url+'trainers/'+str(trainer.id)+'/'
		payload = {
			'last_modified': maya.now().iso8601()
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
	
	def create_update(self, trainer, xp, time_updated=None, **kwargs):
		"""Add a Update object to the database
		
		Arguments:
		trainer - expects a int of trainer's id
		xp
		time_updated - expects datetime.datetime
		dex_caught (optional)
		dex_seen (optional)
		walk_dist (optional)
		gen_1_dex (optional)
		pkmn_caught (optional)
		pkmn_evolved (optional)
		pkstops_spun (optional)
		battles_won (optional)
		gen_2_dex (optional)
		berry_fed (optional)
		gym_defended (optional)
		eggs_hatched (optional)
		big_magikarp (optional)
		legacy_gym_trained (optional)
		tiny_rattata (optional)
		pikachu_caught (optional)
		unown_alphabet (optional)
		raids_completed (optional)
		leg_raids_completed (optional)
		gen_3_dex (optional)
		pkmn_normal (optional)
		pkmn_flying (optional)
		pkmn_poison (optional)
		pkmn_ground (optional)
		pkmn_rock (optional)
		pkmn_bug (optional)pkmn_steel (optional)
		pkmn_fire (optional)
		pkmn_water (optional)
		pkmn_grass (optional)
		pkmn_electric (optional)
		pkmn_psychic (optional)
		pkmn_dark (optional)
		pkmn_fairy (optional)
		pkmn_fighting (optional)
		pkmn_ghost (optional)
		pkmn_ice (optional)pkmn_dragon (optional)
		gym_badges (optional)
		
		"""
		url = api_url+'update/'
		
		payload = {'trainer' : int(trainer),'xp' : int(xp)}
		
		if time_updated is None:
			payload['datetime'] = maya.now().iso8601()
		else:
			payload['datetime'] = time_updated.iso8601()
		if kwargs:
			payload.update(kwargs)
		
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return Update(r.json())
		
	def import_discord_user(self, name, discriminator, id_, avatar_url, creation, user):
		"""Add a discord user"""
		url = api_url+'discord/users/'
		payload = {
			'account': int(user),
			'name': str(name),
			'discriminator': str(discriminator),
			'id': int(id_),
			'avatar_url': str(avatar_url),
			'creation': creation.isoformat()
		}
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return DiscordUser(r.json())
	
	def import_discord_server(self, name, region, id_, owner, icon='https://discordapp.com/assets/2c21aeda16de354ba5334551a883b481.png', bans_cheaters=None, seg_cheaters=None, bans_minors=None, seg_minors=None):
		"""Add a discord server"""
		url = api_url+'discord/servers/'
		payload = {
			'name': str(name),
			'region': str(region),
			'id': int(id_),
			'icon': str(icon),
			'owner': int(owner),
			'bans_cheaters': bans_cheaters,
			'seg_cheaters': seg_cheaters,
			'bans_minors': bans_minors,
			'seg_minors': seg_minors
		}
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return DiscordServer(r.json())
	
	def create_user(self, username, first_name=None, last_name=None):
		"""Create a user"""
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
	
	def get_trainer(self, id_, respect_privacy=True):
		"""Returns the Trainer object for the ID"""
		
		r = requests.get(api_url+'trainers/'+str(id_)+'/')
		print(request_status(r))
		r.raise_for_status()
		return Trainer(r.json(), respect_privacy)
	
	def get_update(self, id_):
		"""Returns the update object for the ID"""
		
		r = requests.get(api_url+'update/'+str(id_)+'/')
		print(request_status(r))
		r.raise_for_status()
		return Update(r.json())
	
	def get_user(self, id_):
		"""Returns the User object for the ID"""
		
		r = requests.get(api_url+'users/'+str(id_)+'/')
		print(request_status(r))
		r.raise_for_status()
		return User(r.json())
	
	def get_discord_user(self, id_):
		"""Returns the User object for the ID"""
		
		r = requests.get(api_url+'discord/users/'+str(id_)+'/')
		print(request_status(r))
		r.raise_for_status()
		return DiscordUser(r.json())
	
	def get_discord_server(self, id_):
		"""Returns the User object for the ID"""
		
		r = requests.get(api_url+'discord/servers/'+str(id_)+'/')
		print(request_status(r))
		r.raise_for_status()
		return DiscordServer(r.json())
	
	def get_all_users(self):
		"""Returns all the users"""
		
		r = requests.get(api_url+'users/')
		print(request_status(r))
		r.raise_for_status()
		user_list = []
		for user in r.json():
			user_list.append(User(user))
		return user_list
	
	def get_all_discord_users(self):
		"""Returns all the discord users"""
		
		r = requests.get(api_url+'discord/users/')
		print(request_status(r))
		r.raise_for_status()
		user_list = []
		for user in r.json():
			user_list.append(DiscordUser(user))
		return user_list
