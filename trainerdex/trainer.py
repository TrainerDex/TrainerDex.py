# -*- coding: utf-8 -*-
import requests
import maya
from .utils import Level
from .http import request_status, api_url
from .update import Update
from .user import User
from .utils import Team

class Trainer:
	"""Reprsents a Trainer Profile"""
	
	def __init__(self, r, respect_privacy=True):
		self.raw = r
		self.id = r['id']
		self.username = r['username']
		self.cheater = r['currently_cheats']
		from .client import Client
		self.team = Client().get_team(r['faction'])
		self.has_cheated = r['has_cheated']
		if r['last_cheated']:
			self.last_cheated = maya.MayaDT.from_iso8601(r['last_cheated']).datetime()
		else:
			self.last_cheated = None
		self.start_date = maya.MayaDT.from_iso8601(r['start_date']).datetime()
		self.goal_daily = r['daily_goal']
		self.goal_total = r['total_goal']
		self.prefered = r['prefered']
		self.account = Client().get_user(r['account'])
		self.update = Update(r['update'])
		self.level = Level().from_xp(self.update.xp)
		self.statistics = r['statistics']
		if self.statistics is False:
			self.account = None
			self.prefered = None
			if respect_privacy is True:
				self.start_date = None
				self.goal_daily = None
				self.goal_total = None
				self.update = None
		
	def __str__(self):
		return "Username: {0.username}, Level: {1}".format(self, Level().from_xp(self.update.xp).level)
	
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
