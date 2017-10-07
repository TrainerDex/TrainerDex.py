# -*- coding: utf-8 -*-
import requests
import json
import datetime
import maya
import inspect
from collections import namedtuple
from utils import Team
from trainer import Trainer
from update import Update
from cached import DiscordUser, DiscordMember, DiscordServer
from http import request_status, api_url

class Client:
	"""Interact with the TrainerDex API
	
	Supply an api token when calling the class.
	"""
	
	def __init__(self, token: str=None):
		headers = {'content-type':'application/json'}
		if token!=None:
			headers['authorization'] = 'Token '+token
		self.headers = headers
	
	@classmethod
	def get_user_from_username(self, username: str):
		"""Returns a User object from a Trainers username"""
		r = requests.get(api_url+'trainers/')
		print(request_status(r))
		r = r.json()
		for i in r:
			if i['username'].lower()==username.lower():
				return User(i['account'])
	
	@classmethod
	def get_teams(self):
		"""Get a list of teams, mostly unchanging so safe to call on init and keep result"""
		teams = []
		for i in 0..3: #Hard coded team IDs, will change if teams ever increase in number
			teams.append(Team(i))
		return teams
		
	def create_trainer(self, username: str, team: int, has_cheated=False, last_cheated: datetime.date=None, currently_cheats=False, statistics=True, daily_goal: int=None, total_goal: int=None, prefered=True, account: int=None):
		"""Add a trainer to the database"""
		url = api_url+'trainers/'
		payload = {
			'username': username,
			'faction': team,
			'has_cheated': has_cheated,
			'last_cheated': last_cheated,
			'currently_cheats': currently_cheats,
			'statistics': statistics,
			'daily_goal': daily_goal,
			'total_goal': total_goal,
			'prefered': prefered,
			'last_modified': maya.now().iso8601(),
			'account': account
		}
		
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return Trainer(int(r.json()['id']))
		
	def update_trainer(cls, username: str=None, has_cheated=None, last_cheated: datetime.date=None, currently_cheats=None, statistics=None, daily_goal: int=None, total_goal: int=None, prefered=None, account: int=None):
		"""Update parts of a trainer in a database"""
		args = locals()
		url = api_url+'trainers/'+str(cls.id_)+'/'
		payload = {
			'last_modified': maya.now().iso8601()
		}
		for i in args:
			if args[i] is not None and i not in ['cls', 'id_', 'cls.id_']:
				payload[i] = args[i]
		r = requests.patch(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return Trainer(int(r.json()['id']))
	
	def create_update(self, trainer: int, xp: int):
		"""Add a Update object to the database"""
		url = api_url+'update/'
		payload = {
			'trainer': trainer,
			'xp': xp,
			'datetime': maya.now().iso8601()
		}
		
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return Update(int(r.json()['id']))
		
	def import_discord_user(self, name: str, discriminator: Union[str,int], id_: Union[str,int], avatar_url: str, creation: datetime.datetime, user: int=None):
		"""Add a discord user"""
		url = api_url+'discord/users/'
		payload = {
			'account': user,
			'name': name,
			'discriminator': discriminator,
			'id': id_,
			'avatar_url': avatar_url,
			'creation': creation.isoformat()
		}
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return DiscordUser(int(r.json()['id']))
	
	def import_discord_server(self, name: str, region: str, id_: Union[str,int], icon: str, owner:int, bans_cheaters=None, seg_cheaters=None, bans_minors=None, seg_minors=None):
		"""Add a discord server"""
		url = api_url+'discord/servers/'
		payload = {
			'name': name,
			'region': region,
			'id': id_,
			'icon': icon,
			'owner': owner,
			'bans_cheaters': bans_cheaters,
			'seg_cheaters': seg_cheaters,
			'bans_minors': bans_minors,
			'seg_minors': seg_minors
		}
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return DiscordServer(int(r.json()['id']))
	
	def import_discord_member(self, user: Union[str,int], server: Union[str,int], join: datetime.datetime):
		"""Add a discord member - stub"""
		pass
#		url = api_url+'discord/users/'
#		payload = {
#			'user': user,
#			'server': server,
#			'join': join.isoformat()
#		}
#		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
#		print(request_status(r))
#		r.raise_for_status()
#		return DiscordMember(int(r.json()['id']))
	
	def create_user(self, username: str, first_name: str=None, last_name: str=None):
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
		return User(int(r.json()['id']))
		
	def update_user(self, username: str=None, first_name: str=None, last_name: str=None):
		"""Update user info"""
		args = locals()
		url = api_url+'users/'+str(cls.id_)+'/'
		payload = {}
		for i in args:
			if args[i] is not None and i not in ['cls', 'id_', 'cls.id_']:
				payload[i] = args[i]
		r = requests.patch(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return User(int(r.json()['id']))
	