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