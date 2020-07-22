from json import loads

class DiscordUser:
	"""Represents a cached Discord user"""
	
	def __init__(self, r):
		self._get = r
		self.id = r['uid']
		self.owner_id = r['user']
	
	def owner(self):
		from .client import Client
		return Client().get_user(self.owner_id)
