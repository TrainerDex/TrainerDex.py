# -*- coding: utf-8 -*-
import maya
from .utils import Level

class Update:
	"""Represents an Update object on the API"""
	
	def __init__(self, r):
		self.raw = r
		try:
			self.id = r['id']
			self.time_updated = maya.MayaDT.from_iso8601(r['datetime']).datetime()
		except KeyError:
			self.id = 0
			self.time_updated = None
		self.xp = r['xp']
		self.dex_caught = r['dex_caught']
		self.dex_seen = r['dex_seen']
		self.walk_dist = r['walk_dist']
		self.gen_1_dex = r['gen_1_dex']
		self.pkmn_caught = r['pkmn_caught']
		self.pkmn_evolved = r['pkmn_evolved']
		self.pkstops_spun = r['pkstops_spun']
		self.battles_won = r['battles_won']
		self.gen_2_dex = r['gen_2_dex']
		self.berry_fed = r['berry_fed']
		self.gym_defended = r['gym_defended']
		self.eggs_hatched = r['eggs_hatched']
		self.big_magikarp = r['big_magikarp']
		self.gyms_trained = r['legacy_gym_trained']
		self.tiny_rattata = r['tiny_rattata']
		self.pikachu_caught = r['pikachu_caught']
		self.unown_alphabet = r['unown_alphabet']
		self.raids_completed = r['raids_completed']
		self.gym_badges = r['gym_badges']
		self.pkmn_normal = r['pkmn_normal']
		self.pkmn_flying = r['pkmn_flying']
		self.pkmn_poison = r['pkmn_poison']
		self.pkmn_ground = r['pkmn_ground']
		self.pkmn_rock = r['pkmn_rock']
		self.pkmn_bug = r['pkmn_bug']
		self.pkmn_steel = r['pkmn_steel']
		self.pkmn_fire = r['pkmn_fire']
		self.pkmn_water = r['pkmn_water']
		self.pkmn_grass = r['pkmn_grass']
		self.pkmn_electric = r['pkmn_electric']
		self.pkmn_psychic = r['pkmn_psychic']
		self.pkmn_dark = r['pkmn_dark']
		self.pkmn_fairy = r['pkmn_fairy']
		self.pkmn_fighting = r['pkmn_fighting']
		self.pkmn_ghost = r['pkmn_ghost']
		self.pkmn_ice = r['pkmn_ice']
		self.pkmn_dragon = r['pkmn_dragon']
	
	@classmethod
	def level(cls):
		return Level().get_by_xp(cls.r['xp'])
	
	@classmethod
	def trainer(cls):
		from .client import Client
		return Client().get_trainer(r['trainer'])
