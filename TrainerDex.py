import requests
import json
import datetime
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

User = namedtuple('User', [
	'id',
	'username',
	'first_name',
	'last_name',
	'dob',
	'profiles',
])

Server = namedtuple('Server', [
	'id',
	'name',
	'region',
	'icon',
	'bans_cheaters',
	'seg_cheaters',
	'bans_minors',
	'seg_minors',
	'owner',
])

Level = namedtuple('Level', [
	'level',
	'total_xp',
	'xp_required'
])

class Requests:
	def __init__(self, token):
		self.url = 'http://127.0.0.1:8000/api/trainer/'
		self.token = token
		self.headers = {'content-type':'application/json', 'authorization':'Token '+token}
		
	def trainerLevels(self, xp=None, level=None):
		levels = [
			Level(level=1,total_xp=0,xp_required=0),
			Level(level=2,total_xp=1000,xp_required=1000),
			Level(level=3,total_xp=3000,xp_required=2000),
			Level(level=4,total_xp=6000,xp_required=3000),
			Level(level=5,total_xp=10000,xp_required=4000),
			Level(level=6,total_xp=15000,xp_required=5000),
			Level(level=7,total_xp=21000,xp_required=6000),
			Level(level=8,total_xp=18000,xp_required=7000),
			Level(level=9,total_xp=36000,xp_required=8000),
			Level(level=10,total_xp=45000,xp_required=9000),
			Level(level=11,total_xp=55000,xp_required=10000),
			Level(level=12,total_xp=65000,xp_required=10000),
			Level(level=13,total_xp=75000,xp_required=10000),
			Level(level=14,total_xp=85000,xp_required=10000),
			Level(level=15,total_xp=100000,xp_required=15000),
			Level(level=16,total_xp=120000,xp_required=20000),
			Level(level=17,total_xp=140000,xp_required=20000),
			Level(level=18,total_xp=160000,xp_required=20000),
			Level(level=19,total_xp=185000,xp_required=25000),
			Level(level=20,total_xp=210000,xp_required=25000),
			Level(level=21,total_xp=260000,xp_required=50000),
			Level(level=22,total_xp=335000,xp_required=75000),
			Level(level=23,total_xp=456000,xp_required=100000),
			Level(level=24,total_xp=560000,xp_required=125000),
			Level(level=25,total_xp=710000,xp_required=150000),
			Level(level=26,total_xp=900000,xp_required=190000),
			Level(level=27,total_xp=1100000,xp_required=200000),
			Level(level=28,total_xp=1350000,xp_required=250000),
			Level(level=29,total_xp=1650000,xp_required=300000),
			Level(level=30,total_xp=2000000,xp_required=350000),
			Level(level=31,total_xp=2500000,xp_required=500000),
			Level(level=32,total_xp=3000000,xp_required=500000),
			Level(level=33,total_xp=3750000,xp_required=750000),
			Level(level=34,total_xp=4750000,xp_required=1000000),
			Level(level=35,total_xp=6000000,xp_required=1250000),
			Level(level=36,total_xp=7500000,xp_required=1500000),
			Level(level=37,total_xp=9500000,xp_required=2000000),
			Level(level=38,total_xp=12000000,xp_required=2500000),
			Level(level=39,total_xp=15000000,xp_required=3000000),
			Level(level=40,total_xp=20000000,xp_required=5000000)
		]
		if level is not None:
			for t in levels:
				if t.level==level:
					return t.total_xp
		elif xp is not None:
			for t in levels:
				if t.total_xp<=xp:
					level = t.level
			return level
		else:
			return levels		
	
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
			t = Trainer(
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
			
		return t, r['statistics']
	
	def getTeams(self):
		r = requests.get(self.url+'factions/').json()
		
		teams = []
		teams_list = r
		for team in teams_list:
			if team['leader_name']:
				leader_name=team['leader_name']
				leader_image=team['leader_image']
			else:
				leader=None
			teams.append(Team(
				id=team['id'],
				name=team['name'],
				colour=team['colour'],
				image=team['logo'],
				leader=leader_name,
				leader_image=leader_image
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
					
	def getUser(self, id):
		id = str(id)
		r = requests.get(self.url+'users/'+id+'/').json()
		extra = r['extended_profile']
		if extra:
			birthday = extra['dob']
		else: birthday = None
		
		profiles=[]
		for profile in r['profiles']:
			profiles.append(profile['username'])
		
		t = User(
			id=r['id'],
			username=r['username'],
			first_name=r['first_name'],
			last_name=r['last_name'],
			dob=birthday,
			profiles=profiles
		)
		
		return t
		
	def getUserByDiscord(self, discord):
		discord = str(discord)
		r = requests.get(self.url+'discord/users/'+discord+'/').json()
		try:
			return self.getUser(r['account']) if r['account'] else None
		except KeyError:
			return None
	
	def getServerInfo(self, server):
		server = str(server)
		r = requests.get(self.url+'discord/servers/'+server+'/').json()
		
		t = Server(
			id=r['id'],
			name=r['name'],
			region=r['region'],
			icon=r['icon'],
			bans_cheaters=r['bans_cheaters'],
			seg_cheaters=r['seg_cheaters'],
			bans_minors=r['bans_minors'],
			seg_minors=r['seg_minors'],
			owner=r['owner']
		)
		return t
		
	def getNetwork(self, network):
		return None #Networks are still under construction
	
	def getBanList(self, server=None, network=None):
		return None #BanList functions as part of Networks
	
	def getReports(self):
		return None #Under construction
		
	def addTrainer(self, username, team, start_date=None, has_cheated=False, last_cheated=None, currently_cheats=False, statistics=True, daily_goal=None, total_goal=None, prefered=True, datetime=str(datetime.datetime.utcnow())):
		url = self.url+'trainers/'
		payload = {
			'username': username,
			'faction': team,
			'has_cheated': has_cheated,
			'last_cheated': last_cheated,
			'currently_cheats': currently_cheats,
			'statistics': statistics,
			'daily_goal': daily_goal,
			'total_goal': total_goal,
			'prefered': prefered,
			'last_modified': datetime
		}
		
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		return r.raise_for_status()
	
	def addUpdate(self, trainer, xp, datetime=str(datetime.datetime.utcnow())):
		url = self.url+'update/'
		payload = {
			'trainer': trainer,
			'xp': xp,
			'datetime': datetime
		}
		
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		return r.raise_for_status()
	
	def addDiscordUser(self, name, discriminator, id, avatar_url, creation, user=None):
		url = self.url+'discord/users/'
		payload = {
			'account': user,
			'name': name,
			'discriminator': discriminator,
			'id': id,
			'avatar_url': avatar_url,
			'creation': creation
		}
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		return r.raise_for_status()
	
	def addDiscordServer(self, name, region, id, icon, owner, bans_cheaters=None, seg_cheaters=None, bans_minors=None, seg_minors=None):
		url = self.url+'discord/servers/'
		payload = {
			'name': name,
			'region': region,
			'id': id,
			'icon': icon,
			'owner': owner,
			'bans_cheaters': bans_cheaters,
			'seg_cheaters': seg_cheaters,
			'bans_minors': bans_minors,
			'seg_minors': seg_minors
		}
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		return r.raise_for_status()
	
#	def addDiscordMember(self, user, server, join):
#		url = self.url+'discord/users/'
#		payload = {
#			'user': user,
#			'server': server,
#			'join': join
#		}
#		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
#		return r.raise_for_status()
	
	def addUserAccount(self, username, first_name=None, last_name=None):
		url = self.url+'users/'
		payload = {
			'username':username
		}
		if first_name:
			payload['first_name'] = first_name
		if last_name:
			payload['last_name'] = last_name
		r = requests.post(url, data=json.dumps(payload), headers=self.headers)
		if r.raise_for_status() is not None:
			return r.raise_for_status()
		else: 
			return r.json()['id']