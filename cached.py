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

class DiscordMember(DiscordUser):
	"""Represents a cached Discord member"""
	
	def __init__(self, id_, server):
		super().__init__(id_)
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