import requests
from collections import namedtuple

Trainer = namedtuple('Trainer', [
	'username',
	'start_date',
	'has_cheated',
	'last_cheated',
	'cheater',
	'goal_daily',
	'goal_total',
	'prefered',
	'account_ID',
	'team',
	'xp',
	'xp_time',
])

Team = namedtuple('Team', [
	'id',
	'name',
	'colour',
	'leader'
])

Update = namedtuple('Update', [
	'time_updated',
	'total_xp',
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

class Requests:
	def __init__(self, token):
		self.url = 'http://127.0.0.1:8000/api/trainer/'
		self.token = token
	
	def getTrainer(self, name, force=False):
		r = requests.get(self.url+'trainers/'+name+'/').json()
		updates = r['update']
		if r['statistics'] is False and force is False:
			trainer = Trainer(
				username = r['username'],
				start_date = None,
				has_cheated = r['has_cheated'],
				last_cheated = r['last_cheated'],
				cheater = r['currently_cheats'],
				goal_daily = None,
				goal_total = None,
				prefered = None,
				account_ID = None,	
				team = r['faction'],
				xp = None,
				xp_time = None
			)
		elif r['statistics'] is False and force is True:
			trainer = Trainer(
				username = r['username'],
				start_date = r['start_date'],
				has_cheated = r['has_cheated'],
				last_cheated = r['last_cheated'],
				cheater = r['currently_cheats'],
				goal_daily = r['daily_goal'],
				goal_total = r['total_goal'],
				prefered = None,
				account_ID = None,	
				team = r['faction'],
				xp = updates['xp'],
				xp_time = updates['datetime']
			)
		else:
			trainer = Trainer(
				username = r['username'],
				start_date = r['start_date'],
				has_cheated = r['has_cheated'],
				last_cheated = r['last_cheated'],
				cheater = r['currently_cheats'],
				goal_daily = r['daily_goal'],
				goal_total = r['total_goal'],
				prefered = r['prefered'],
				account_ID = r['account'],	
				team = r['faction'],
				xp = updates['xp'],
				xp_time = updates['datetime']
			)
			
		return trainer, r['statistics']
	
	def getTeams(self):
		r = requests.get(self.url+'factions/').json()
		
		teams = []
		teams_list = r
		for team in teams_list:
			if team['leader_name']:
				leader=team['leader_name']
			else:
				leader=None
			teams.append(Team(
				id=team['id'],
				name=team['name'],
				colour=team['colour'],
				leader=leader
			))
		
		return teams
	
	def getUpdates(self, trainer):
		r = requests.get(self.url+'update/').json()
		
		updates = []
		update_list = r
		for update in update_list:
			if update['trainer']==trainer:
				updates.append(Update(
					time_updated=update['datetime'],
					total_xp=update['xp'],
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
				))
			
		return None if updates==[] else updates
					
		