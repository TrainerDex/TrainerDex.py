# -*- coding: utf-8 -*-
import maya
from .utils import Level
from .update import Update

class Trainer:
	"""Reprsents a Trainer Profile"""
	
	def __init__(self, r, respect_privacy=True):
		self.raw = r
		self.id = r['id']
		self.username = r['username']
		self.cheater = r['currently_cheats']
		self.has_cheated = r['has_cheated']
		if r['last_cheated']:
			self.last_cheated = maya.MayaDT.from_iso8601(r['last_cheated']).datetime()
		else:
			self.last_cheated = None
		if r['start_date']:
			self.start_date = maya.MayaDT.from_iso8601(r['start_date']).datetime()
		else:
			self.start_date = None
		self.goal_daily = r['daily_goal']
		self.goal_total = r['total_goal']
		self.prefered = r['prefered']
		self.update = Update(r['update'])
		try:
			self.level = Level().from_xp(self.update.xp)
		except TypeError:
			self.level = None
		self.statistics = r['statistics']
		if self.statistics is False and respect_privacy is True:
			self.start_date = None
			self.goal_daily = None
			self.goal_total = None
			self.update = None
		
	def __str__(self):
		return self.username
	
	def __hash__(self):
		return self.id
	
	def __eq__(self, other):
		return self.id == other.id
	
	def updates(self):
		_updates = self.raw['updates']
		updates = []
		for json in _updates:
			updates.append(Update(json))
		updates.sort(key=lambda x:x.time_updated, reverse=True)
		return updates
	
	def team(self):
		from .client import Client
		return Client().get_team(self.raw['faction'])
	
	def owner(self):
		from .client import Client
		return Client().get_user(self.raw['account'])
	
	account = owner
