import requests
import iso8601
from collections import namedtuple

api_url = 'http://www.ekpogo.uk/api/trainer/'

Trainer = namedtuple('Trainer', [
	'id',
	'username',
	'start_date',
	'has_cheated',
	'last_cheated',
	'cheater',
	'goal_daily',
	'goal_total',
	'prefered',
	'account',
	'team',
	'xp',
	'xp_time',
	'statistics',
])

TrainerList = namedtuple('TrainerList', [
	'username',
	'id',
	'account',
	'discord',
	'team',
	'prefered'
])

Team = namedtuple('Team', [
	'id',
	'name',
	'colour',
	'image',
	'leader',
	'leader_image',
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

DiscordMember = namedtuple('DiscordMember', [
	'discord_id',
	'account_id',
	'name',
	'unique',
	'avatar',
	'creation',
	'joined'
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
		#update = r['update']
		#self.xp = update['xp']
		#self.xp_time = iso8601.parse_date(update['datetime'])
		self.statistics = r['statistics']
		if self.statistics is False:
			self.account = None
			self.prefered = Nine
			if force is False:
				self.start_date=None
				self.goal_daily=None
				self.goal_total=None
				#self.xp=None
				#self.xp_time=None
		
	@classmethod
	def level(cls):
		return Level().get_by_xp(cls.update['xp'])