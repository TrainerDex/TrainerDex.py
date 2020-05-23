from .update import Update

try:
	from maya import MayaDT
except ModuleNotFoundError:
	import dateutil.parser
	MayaDT = None

class Trainer:
	"""Reprsents a Trainer Profile"""
	
	def __init__(self, r):
		self._get = r
		self.id = r['id']
		self.username = r['username']
		if MayaDT:
			self.start_date = MayaDT.from_iso8601(r['start_date']).datetime() if r['start_date'] else None
		else:
			self.start_date = dateutil.parser.parse(r['start_date']) if r['start_date'] else None
		self.cheater = r['currently_cheats']
		self.has_cheated = r['has_cheated']
		if MayaDT:
			self.last_cheated = MayaDT.from_iso8601(r['last_cheated']).datetime() if r['last_cheated'] else None
		else:
			self.last_cheated = dateutil.parser.parse(r['last_cheated']) if r['last_cheated'] else None
		self.goal_daily = r['daily_goal']
		self.goal_total = r['total_goal']
		self.prefered = r['prefered']
		self.update = Update(r['update_set'][0]) if r['update_set'] else None
		self.level = self.update.level() if self.update else None
		
	def __str__(self):
		return self.username
	
	def __hash__(self):
		return self.id
	
	def __eq__(self, other):
		return self.id == other.id
	
	def updates(self):
		updates = []
		for x in self._get['update_set']:
			updates.append(Update(x))
		updates.sort(key=lambda x:x.update_time, reverse=True)
		return updates
	
	def team(self):
		from .utils import get_team
		return get_team(self._get['faction'])
	
	def owner(self):
		from .client import Client
		return Client().get_user(self._get['owner'])
