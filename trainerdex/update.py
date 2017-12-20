# -*- coding: utf-8 -*-
import maya
from .utils import level_parser

class Update:
	"""Represents an Basic Update object on the API"""
	
	def __init__(self, r):
		self._get = r
		self.uuid = r['uuid']
		self.update_time = maya.MayaDT.from_iso8601(r['update_time']).datetime()
		self.xp = r['xp']
	
	def level(self):
		return level_parser(xp=self.xp)
	
	def trainer(cls):
		from .client import Client
		return Client().get_trainer(self._get['trainer'])
