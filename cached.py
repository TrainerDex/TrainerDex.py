# -*- coding: utf-8 -*-
import requests
import maya
from http import request_status, api_url
from user import User

class DiscordUser:
	"""Represents a cached Discord user"""
	
	def __init__(self, id_):
		r = requests.get(api_url+'discord/users/'+str(id_)+'/')
		self.status = request_status(r)
		print(self.status)
		r.raise_for_status()
		r = r.json()
		self.raw = r
		self.id = r['id']
		self.name = r['name']
		self.discriminator = r['discriminator']
		self.avatar_url = r['avatar_url']
		self.creation = maya.MayaDT.from_iso8601(r['creation']).datetime()
		self.owner = User(int(r['account']))
		
	@classmethod
	def update(self, name: str, discriminator: Union[str,int], avatar_url: str):
		"""Update information about a discord user"""
		url = api_url+'discord/users/'+str(cls.id_)+'/'
		payload = {
			'name': name,
			'discriminator': str(discriminator)
			'avatar_url': avatar_url
		}
		r = requests.patch(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return DiscordUser(int(r.json()['id']))

class DiscordMember(DiscordUser):
	"""Represents a cached Discord member"""
	
	def __init__(self, id_, server):
		super().__init__(id_)
		pass
#		r = requests.get(api_url+'discord/members/'+str(id_)+'/')
#		self.status = request_status(r)
#		print(self.status)
#		r.raise_for_status()
#		r = r.json()
#		self.raw = [self.raw, r]
#		self.server = Server(r['server'])
#		self.join = maya.MayaDT.from_iso8601(r['join']).datetime()
	
	@classmethod
	def update(cls):
		pass

class DiscordServer:
	"""Represents a cached Discord server"""
	
	def __init__(self, id_):
		r = requests.get(api_url+'discord/servers/'+str(id_)+'/')
		self.status = request_status(r)
		print(self.status)
		r.raise_for_status()
		r = r.json()
		self.raw = r
		self.id = r['id']
		self.name = r['name']
		self.region = r['region']
		self.icon = r['icon']
		if r['bans_cheaters'] is True:
			self.cheaters = 2
		elif r['seg_cheaters'] is True:
			self.cheaters = 1
		else:
			self.cheaters = 0
		if r['bans_minors'] is True:
			self.minors = 2
		elif r['seg_minors'] is True:
			self.minors = 1
		else:
			self.minors = 0
		self.owner = Member(int(r['owner']), self.id)
		
	@classmethod
	def update(self, name: str, region: str, id_: Union[str,int], icon: str, owner: int, bans_cheaters=None, seg_cheaters=None, bans_minors=None, seg_minors=None):
		"""Update information about a discord server"""
		url = api_url+'discord/users/'+str(cls.id_)+'/'
		payload = {
			'name': name,
			'region': region,
			'icon': icon,
			'owner': owner,
		}
		#Cheaters and Minors functions aren't currently automated.
		r = requests.patch(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return DiscordUser(int(r.json()['id']))
		