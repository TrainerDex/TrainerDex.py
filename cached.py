# -*- coding: utf-8 -*-
import requests
import iso8601
from client import http_url as api_url

class DiscordUser:
	"""Represents a cached Discord user"""
	
	def __init__(self, id):
		r = requests.get(api_url+'discord/users/'+str(id)+'/')
		self.status = r.status_code
		r = r.json()
		self.raw = r
		self.id = r['id']
		self.name = r['name']
		self.discriminator = r['discriminator']
		self.avatar_url = r['avatar_url']
		self.creation = iso8601.parse_date(r['creation'])
		self.owner = r['account']

class DiscordMember(DiscordUser):
	"""Represents a cached Discord member"""
	
	def __init__(self, id, server):
		super().__init__(id)
#		r = requests.get(api_url+'discord/members/'+str(id)+'/')
#		self.status = [self.status, r.status_code]
#		r = r.json()
#		self.raw = [self.raw, r]
#		self.server = Server(r['server'])
#		self.join = iso8601.parse_date(r['join'])

class DiscordServer:
	"""Represents a cached Discord server"""
	
	def __init__(self, id):
		r = requests.get(api_url+'discord/servers/'+str(id)+'/')
		self.status = r.status_code
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