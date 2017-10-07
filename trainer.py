# -*- coding: utf-8 -*-
import requests
import maya
from utils import Level
from http import request_status, api_url
from update import Update
from user import User
from utils import Team

class Trainer:
	"""Get information about a trainer"""
	
	def __init__(self, id_: int, force=False):
		r = requests.get(api_url+'trainers/'+str(id_)+'/')
		self.status = request_status(r)
		print(self.status)
		r.raise_for_status()
		r = r.json()
		self.raw = r
		self.id = r['id']
		self.username = r['username']
		self.cheater = r['currently_cheats']
		self.team = Team(r['faction'])
		self.has_cheated = r['has_cheated']
		if r['last_cheated']:
			self.last_cheated = maya.MayaDT.from_iso8601(r['last_cheated']).datetime()
		else:
			self.last_cheated = None
		self.start_date = maya.MayaDT.from_iso8601(r['start_date']).datetime()
		self.goal_daily = r['daily_goal']
		self.goal_total = r['total_goal']
		self.prefered = r['prefered']
		self.account = User(int(r['account']))
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
	def all_updates(cls):
		"""Get a list of all update objects by trainer in date order of newest first"""
		r = requests.get(api_url+'update/')
		print(request_status(r))
		r.raise_for_status()
		r = r.json()
		updates = []
		for update in r:
			if update['trainer']==trainer:
				updates.append(Update(update['id']))
		
		return updates.sort(key=lambda x:x.time_updated, reverse=True)
