from json import loads

class DiscordUser:
	"""Represents a cached Discord user"""
	
	def __init__(self, r):
		self._get = r
		self.id = r['uid']
		self._extra_data = loads(r['extra_data'].replace("True", "true").replace("False", "false")) # Compensates for invalid JSON in API
		try:
			self.username = self._extra_data['username'] or None
		except KeyError:
			self.username = None
		try:
			self.discriminator = self._extra_data['discriminator'] or None
		except KeyError:
			self.discriminator = None
		self.owner_id = r['user']
	
	def owner(self):
		from .client import Client
		return Client().get_user(self.owner_id)
