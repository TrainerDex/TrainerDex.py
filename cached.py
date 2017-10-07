# -*- coding: utf-8 -*-
import requests
import maya
import discord
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

class refresh_discord:
	"""Refresh all instances of cached users and servers
	
	Arguments:
	bot - Bot should be a discord.Client() with a valid token. If you're using discord caching functions, you're likely already using a discord.py bot. Just pass this over in the bot arg
	client - Client should be the trainerdex.Client() with a valid token.
	
	You've likely already declared these two, just pass them through.
	"""
	
	def __init__(self, discordClient, client):
	self.bot = discordClient # Bot should be a discord.Client() with a valid token. If you're using discord caching functions, you're likely already using a discord.py bot. Just pass this over in the bot arg
	self.client = client # Client should be the trainerdex.Client() with a valid token.
	
	@classmethod
	def servers(cls):
		bot = cls.self.bot
		client = cls.self.client
		cached_servers = requests.get(api_url+'discord/servers/')
		print(request_status(cached_servers))
		cached_servers.raise_for_status()
		cached_servers = cached_servers.json()
		cached_server_ids = []
		for server in cached_servers:
			cached_server_ids.append(server['id'])
		client_servers = bot.servers
		for server in client_servers:
			if server.id in cached_server_ids:
				url = api_url+'discord/servers/'+str(server.id)+'/'
				payload = {
					'name': server.name,
					'region': str(server.region),
					'icon': server.icon_url,
					'owner': server.owner.id
					}
				patch = requests.patch(url, data=json.dumps(payload), headers=client.headers)
				print(request_status(patch))
				patch.raise_for_status()
			url = None
			payload = None
			patch = None

 
