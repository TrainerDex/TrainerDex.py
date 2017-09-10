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

class Requests:
	def __init__(self, token):
		self.url = "http://127.0.0.1:8000/api/trainer"
		self.token = token
	
	def getTrainer(name):
		r = requests.get(self.url+'/'+'trainers/'+name+'/').json()
		updates = r['update']
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
			
		return trainer