# -*- coding: utf-8 -*-
import requests
from .http import request_status, api_url

class User:
	"""Represents a user"""
	
	def __init__(self, r):
		self.raw = r
		self.id = r['id']
		print('trainerdex.User({})'.format(self.id))
		self.username = r['username']
		self.first_name = r['first_name']
		self.last_name = r['last_name']
		#xprofile = None #Extended Profiles are still under construction
		#self.dob = None
		#self.birthday = self.dob
		
	def trainer(self, all_=False):
		from .trainer import Trainer
		_profiles = self.raw['profiles']
		profiles = []
		for i in _profiles:
			if all_==False:
				if i['prefered']==True:
					profiles = Trainer(i)
			if all_==True:
				profiles.append(Trainer(i))
		return profiles
		
	def discord(self):
		from .cached import DiscordUser
		r = requests.get(api_url+'discord/users/')
		print(request_status(r))
		r.raise_for_status()
		r = r.json()
		for i in r:
			if i['account']==self.id:
				return DiscordUser(i)
	
	def __hash__(self):
		return self.id
	
	def __eq__(self, other):
		return self.id == other.id
