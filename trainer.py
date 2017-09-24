# -*- coding: utf-8 -*-
import requests
import iso8601
from collections import namedtuple
from utils import Level
from client import http_url as api_url

Update = namedtuple('Update', [
	'time_updated',
	'xp',
	'dex_caught',
	'dex_seen',
	'walk_dist',
	'gen_1_dex',
	'pkmn_caught',
	'pkmn_evolved',
	'pkstops_spun',
	'battles_won',
	'gen_2_dex',
	'berry_fed',
	'gym_defended',
	'eggs_hatched',
	'big_magikarp',
	'gyms_trained',
	'tiny_rattata',
	'pikachu_caught',
	'unown_alphabet',
	'raids_completed',
	'gym_badges',
	'pkmn_normal',
	'pkmn_flying',
	'pkmn_poison',
	'pkmn_ground',
	'pkmn_rock',
	'pkmn_bug',
	'pkmn_steel',
	'pkmn_fire',
	'pkmn_water',
	'pkmn_grass',
	'pkmn_electric',
	'pkmn_psychic',
	'pkmn_dark',
	'pkmn_fairy',
	'pkmn_fighting',
	'pkmn_ghost',
	'pkmn_ice',
	'pkmn_dragon',
])

class Trainer:
	"""Get information about a trainer"""
	
	def __init__(self, id, force=False):
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
		self.account = r['account']
		update = r['update']
		self.update = Update(
			time_updated=iso8601.parse_date(update['datetime']),
			xp=update['xp'],
			dex_caught=update['dex_caught'],
			dex_seen=update['dex_seen'],
			walk_dist=update['walk_dist'],
			gen_1_dex=update['gen_1_dex'],
			pkmn_caught=update['pkmn_caught'],
			pkmn_evolved=update['pkmn_evolved'],
			pkstops_spun=update['pkstops_spun'],
			battles_won=update['battles_won'],
			gen_2_dex=update['gen_2_dex'],
			berry_fed=update['berry_fed'],
			gym_defended=update['gym_defended'],
			eggs_hatched=update['eggs_hatched'],
			big_magikarp=update['big_magikarp'],
			gyms_trained=update['legacy_gym_trained'],
			tiny_rattata=update['tiny_rattata'],
			pikachu_caught=update['pikachu_caught'],
			unown_alphabet=update['unown_alphabet'],
			raids_completed=update['raids_completed'],
			gym_badges=update['gym_badges'],
			pkmn_normal=update['pkmn_normal'],
			pkmn_flying=update['pkmn_flying'],
			pkmn_poison=update['pkmn_poison'],
			pkmn_ground=update['pkmn_ground'],
			pkmn_rock=update['pkmn_rock'],
			pkmn_bug=update['pkmn_bug'],
			pkmn_steel=update['pkmn_steel'],
			pkmn_fire=update['pkmn_fire'],
			pkmn_water=update['pkmn_water'],
			pkmn_grass=update['pkmn_grass'],
			pkmn_electric=update['pkmn_electric'],
			pkmn_psychic=update['pkmn_psychic'],
			pkmn_dark=update['pkmn_dark'],
			pkmn_fairy=update['pkmn_fairy'],
			pkmn_fighting=update['pkmn_fighting'],
			pkmn_ghost=update['pkmn_ghost'],
			pkmn_ice=update['pkmn_ice'],
			pkmn_dragon=update['pkmn_dragon']
			)
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
	