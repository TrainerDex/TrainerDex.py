# -*- coding: utf-8 -*-
import requests
import maya
from .http import request_status, api_url
from .user import User

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
	
	def get_trainers(self, discord_server):
		member_list = discord_server.members
		trainer_list = []
		for member in member_list:
			try:
				trainer_list.append(DiscordUser(member.id).owner.trainer(all_=False))
			except requests.exceptions.HTTPError:
				pass
		return member_list

class refresh_discord:
	"""Refresh all seen instances of cached users and servers
	
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
	
	@classmethod
	def users(cls):
		bot = cls.self.bot
		client = cls.self.client
		cached_users = requests.get(api_url+'discord/users/')
		print(request_status(cached_users))
		cached_users.raise_for_status()
		cached_users = cached_users.json()
		cached_user_ids = []
		for user in cached_users:
			cached_user_ids.append(int(user['id']))
		client_users = bot.get_all_members()
		for user in client_users:
			if int(user.id) in cached_user_ids:
				url = api_url+'discord/servers/'+str(user.id)+'/'
				payload = {
					'name': user.name,
					'discriminator': str(user.discriminator),
					'avatar_url': user.avatar_url
					}
				patch = requests.patch(url, data=json.dumps(payload), headers=client.headers)
				print(request_status(patch))
				patch.raise_for_status()
			url = None
			payload = None
			patch = None