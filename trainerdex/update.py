from .utils import level_parser

try:
	from maya import MayaDT
except ModuleNotFoundError:
	import dateutil.parser
	MayaDT = None

class Update:
	"""Represents an Basic Update object on the API"""
	
	def __init__(self, r):
		self._get = r
		self.uuid = r['uuid']
		if MayaDT:
			self.update_time = MayaDT.from_iso8601(r['update_time']).datetime()
		else:
			self.update_time = dateutil.parser.parse(r['update_time'])
		self.xp = r['xp']
	
	def level(self):
		return level_parser(xp=self.xp)
	
	def trainer(cls):
		from .client import Client
		return Client().get_trainer(self._get['trainer'])
