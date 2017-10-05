# -*- coding: utf-8 -*-
import requests
import iso8601
from utils import Level
from client import http_url as api_url
from update import Update
from user import User

class Trainer:
	"""Get information about a trainer"""
	
	def __init__(self, id: int, force=False):
		r = requests.get(api_url+'trainers/'+str(id)+'/')
		self.status = r.status_code
		r = r.json()
		self.raw = r
		self.id = r['id']
		self.username = r['username']
		self.cheater = r['currently_cheats']
		self.team = r['faction']
		self.has_cheated = r['has_cheated']
		self.last_cheated = r['last_cheated']
		self.start_date = r['start_date']
		self.goal_daily = r['daily_goal']
		self.goal_total = r['total_goal']
		self.prefered = r['prefered']
		self.account = Trainer(int(r['account']))
		update = r['update']
		self.update = Update(update['id'])
		self.statistics = r['statistics']
		if self.statistics is False:
			self.account = None
			self.prefered = None
			if force is False:
				self.start_date = None
				self.goal_daily = None
				self.goal_total = None
				self.update = None
		
	def __str__(self):
		return "Username: {0.username}, Level: {1}".format(self, Level().from_xp(self.update.xp).level)
		
	@classmethod
	def level(cls):
		return Level().get_by_xp(cls.update['xp'])
		
	@classmethod
	def get_updates(cls):
		"""Get a list of all update objects by trainer"""
		r = requests.get(api_url+'update/')
		if r.status_code==200:
			print("{}: OK".format(inspect.currentframe().f_code.co_name,r.status_code))
		else:
			print("{}: {} - {}".format(inspect.currentframe().f_code.co_name,r.status_code ,r.json()))
		r = r.json()
		updates = []
		for update in r:
			if update['trainer']==trainer:
				updates.append(Update(update['id']))
		
		return updates
	