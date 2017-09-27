# -*- coding: utf-8 -*-
import requests
import json
import datetime
import iso8601
import inspect
from collections import namedtuple
from utils import Team

User = namedtuple('User', [
	'id',
	'username',
	'first_name',
	'last_name',
	'dob',
	'profiles',
])

http_url = 'http://www.ekpogo.uk/api/trainer/'

class Requests:
	"""Interact with the TrainerDex API
	
	Supply an api token when calling the class.
	"""
	
	def __init__(self, token: str=None):
		self.url = http_url
		self.headers = {'content-type':'application/json'}
		if token:
			self.headers['authorization'] = 'Token '+token
		
	def listDiscordUsers(self):
		"""Get a list of all seen discord users"""
		r = requests.get(self.url+'discord/users/')
		if r.status_code==200:
			print("{}: {}".format(inspect.currentframe().f_code.co_name,r.status_code))
		else:
			print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
		r = r.json()
		users = []
		for user in r:
			users.append(DiscordMember(
			discord_id = user['id'],
			account_id = user['account'],
			name = user['name'],
			unique = user['discriminator'],
			avatar = user['avatar_url'],
			creation = iso8601.parse_date(user['creation']),
			joined = None
		))
		
		return users
		
	def listTrainers(self):
		"""Get a list of all trainers and their linked ekpogo account and discord account"""
		r = requests.get(self.url+'trainers/')
		if r.status_code==200:
			print("{}: {}".format(inspect.currentframe().f_code.co_name,r.status_code))
		else:
			print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
		r = r.json()
		trainers = []
		discord=None
		listDiscordUsers=self.listDiscordUsers()
		for trainer in r:
			for user in listDiscordUsers:
				if user.account_id==trainer['account']:
					discord = user.discord_id
			
			trainers.append(TrainerList(
				username = trainer['username'],
				id = trainer['id'],
				account = trainer['account'],
				discord = discord,
				team = trainer['faction'],
				prefered = trainer['prefered']
			))
		
		return trainers
	
	def get_teams(self):
		"""Get a list of teams, mostly unchanging so safe to call on init and keep result"""
		teams = []
		for i in 0..3: #Hard coded team IDs, will change if teams ever increase in number
			teams.append(Team(i))
		return teams
					
	def getUser(self, id: Union[str,int]):
		"""Get information about a user, including a list of all trainers associated"""
		id = str(id)
		r = requests.get(self.url+'users/'+str(id)+'/')
		print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
		r = r.json()
#		extra = r['extended_profile']
		extra = None
		if extra:
			birthday = iso8601.parse_date(extra['dob'])
			birthday = birthday.date()
		else: birthday = None
		
		profiles=[]
		for profile in r['profiles']:
			profiles.append(profile['username'])
		
		t = User(
			id=r['id'],
			username=r['username'],
			first_name=r['first_name'],
			last_name=r['last_name'],
			dob=birthday,
			profiles=profiles
		)
		
		return t
		
	def getUserByDiscord(self, discord: Union[str,int]):
		"""Get a user object via their discord ID instead of user ID"""
		r = requests.get(self.url+'discord/users/'+str(discord)+'/')
		print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
		r = r.json()
		try:
			return self.getUser(r['account']) if r['account'] else None
		except KeyError:
			return None
	
	def getNetwork(self, network):
		"""Networks are still under construction"""
		pass
	
	def getBanList(self, server=None, network=None):
		"""BanList functions as part of Networks"""
		pass
	
	def getReports(self):
		"""Under construction"""
		pass
		
	def addTrainer(self, username: str, team: int, has_cheated=False, last_cheated: datetime.date=None, currently_cheats=False, statistics=True, daily_goal: int=None, total_goal: int=None, prefered=True, datetime=datetime.datetime.utcnow(), account: int=None):
		"""Add a trainer to the database"""
		url = self.url+'trainers/'
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
			'last_modified': datetime.isoformat(),
			'account': account
		}
		
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
		status = r.raise_for_status()
		if status is not None:
			return status
		else:
			return r.json()['id']
		
	def patchTrainer(self, id: int, username: str=None, has_cheated=None, last_cheated: datetime.date=None, currently_cheats=None, statistics=None, daily_goal: int=None, total_goal: int=None, prefered=None, account: int=None):
		"""Update parts of a trainer in a database"""
		pass
		args = locals()
		url = self.url+'trainers/'+str(id)+'/'
		updated=datetime.datetime.utcnow()
		payload = {
			'last_modified': updated.isoformat()
		}
		for i in args:
			if args[i] is not None and i not in ['self','id']:
				payload[i] = args[i]
		r = requests.patch(url, data=json.dumps(payload), headers=self.headers)
		print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code, r.json()))
		status = r.raise_for_status()
		return status
	
	def addUpdate(self, trainer: int, xp: int, datetime=:datetime.datetime = datetime.datetime.utcnow()):
		"""Add a Update object to the database"""
		url = self.url+'update/'
		payload = {
			'trainer': trainer,
			'xp': xp,
			'datetime': datetime.isoformat()
		}
		
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
		status = r.raise_for_status()
		if status is not None:
			return status
		else:
			return r.json()['id']
	
	def patchDiscordUser(self, name: str, discriminator: Union[str,int], id: Union[str,int], avatar_url: str, creation: datetime:datetime, user: int=None):
		"""Update information about a discord user"""
		url = self.url+'discord/users/'+str(id)+'/'
		payload = {
			'account': user,
			'name': name,
			'discriminator': discriminator,
			'id': id,
			'avatar_url': avatar_url,
			'creation': creation.isoformat()
		}
		r = requests.patch(url, data=json.dumps(payload), headers=self.headers)
		print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
		status = r.raise_for_status()
		if status is not None:
			return status
		else:
			return r.json()['id']
		
	def addDiscordUser(self, name: str, discriminator: Union[str,int], id: Union[str,int], avatar_url: str, creation: datetime:datetime, user: int=None):
		"""Add a discord user"""
		url = self.url+'discord/users/'
		payload = {
			'account': user,
			'name': name,
			'discriminator': discriminator,
			'id': id,
			'avatar_url': avatar_url,
			'creation': creation.isoformat()
		}
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
		status = r.raise_for_status()
		if status is not None:
			return status
		else:
			return r.json()['id']
	
	def addDiscordServer(self, name: str, region: str, id: Union[str,int], icon: str, owner:int, bans_cheaters=None, seg_cheaters=None, bans_minors=None, seg_minors=None):
		"""Add a discord server"""
		url = self.url+'discord/servers/'
		payload = {
			'name': name,
			'region': region,
			'id': id,
			'icon': icon,
			'owner': owner,
			'bans_cheaters': bans_cheaters,
			'seg_cheaters': seg_cheaters,
			'bans_minors': bans_minors,
			'seg_minors': seg_minors
		}
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
		status = r.raise_for_status()
		if status is not None:
			return status
		else:
			return r.json()['id']
	
	def addDiscordMember(self, user: Union[str,int], server: Union[str,int], join: datetime.datetime):
		"""Add a discord member - stub"""
		pass
#		url = self.url+'discord/users/'
#		payload = {
#			'user': user,
#			'server': server,
#			'join': join.isoformat()
#		}
#		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
#		print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
#		return r.raise_for_status()
	
	def addUserAccount(self, username: str, first_name: str=None, last_name: str=None):
		"""Create a user"""
		url = self.url+'users/'
		payload = {
			'username':username
		}
		if first_name:
			payload['first_name'] = first_name
		if last_name:
			payload['last_name'] = last_name
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
		status = r.raise_for_status()
		if status is not None:
			return status
		else:
			return r.json()['id']
		
	def patchUserAccount(self, id: int, username: str=None, first_name: str=None, last_name: str=None):
		"""Update user info"""
		url = self.url+'users/'+str(id)+'/'
		payload = {}
		if username:
			payload['username'] = username
		if first_name:
			payload['first_name'] = first_name
		if last_name:
			payload['last_name'] = last_name
		r = requests.patch(url, data=json.dumps(payload), headers=self.headers)
		print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
		status = r.raise_for_status()
		if status is not None:
			return status
		else:
			return r.json()['id']