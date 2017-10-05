# -*- coding: utf-8 -*-
import requests
from http import request_status, api_url
from trainer import Trainer

class User:
	"""Represents a user"""
	
	def __init__(self, id_):
		r = requests.get(api_url+'users/'+str(id_)+'/')
		self.status = request_status(r)
		print(self.status)
		r.raise_for_status()
		r = r.json()
		self.raw = r
		self.id = r['id']
		self.username = r['username']
		self.first_name = r['first_name']
		self.last_name = r['last_name']
		xprofile = None #Extended Profiles are still under construction
		self.dob = None
		self.birthday = self.dob
		
	@classmethod
	def trainer(cls, show_all=False):
		_profiles = cls.r['profiles']
		profiles = []
		for i in _profiles:
			if i.prefered==True:
				profiles.append(Trainer(i))
		if show_all==True:
			for i in _profiles:
				if i.prefered==False:
					profiles.append(Trainer(i))
		return profiles
		
	@classmethod
	def discord(cls):
		r = requests.get(api_url+'discord/users/')
		print(request_status(r))
		r.raise_for_status()
		r = r.json()
		for i in r:
			if i['account']==cls.id_:
				return DiscordUser(i)
	
	@classmethod
	def update(self, username: str=None, first_name: str=None, last_name: str=None):
		"""Update user info"""
		args = locals()
		url = api_url+'users/'+str(cls.id_)+'/'
		payload = {}
		for i in args:
			if args[i] is not None and i not in ['cls', 'id_', 'cls.id_']:
				payload[i] = args[i]
		r = requests.patch(url, data=json.dumps(payload), headers=self.headers)
		print(request_status(r))
		r.raise_for_status()
		return User(int(r.json()['id']))
		