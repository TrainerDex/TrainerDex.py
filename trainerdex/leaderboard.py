from .trainer import Trainer
from warnings import warn
from maya import MayaDT

class LeaderboardInstance:
	
	def __init__(self, r):
		self._get = r
		self._position = r['position']
		self._trainer_id = r['id']
		self._trainer_username = r['username']
		self._user_id = r['user_id']
		self._xp = int(r['xp'])
		self._time = MayaDT.from_iso8601(r['last_updated']).datetime()
		self._level = int(r['level'])
		self._faction = r['faction']
	
	@property
	def position(cls):
		return cls._position
	
	@property
	def trainer(cls, detail=False):
		from .client import Client
		
		if detail == False:
			return Trainer(
				{
					'id': cls._trainer_id,
					'username': cls._trainer_username,
					'start_date': None,
					'currently_cheats': None,
					'has_cheated': None,
					'last_cheated': None,
					'daily_goal': None,
					'total_goal': None,
					'prefered': True,
					'update_set': None,
					'faction': cls._faction['id'],
					'owner': cls._user_id
				})
		elif detail == True:
			return Client().get_trainer(id_=cls._trainer_id, respect_privacy=False)
	
	@property
	def owner(cls):
		from .client import Client
		
		return Client().get_user(cls._user_id)
	
	@property
	def xp(cls):
		return cls._xp
	
	@property
	def time(cls):
		return cls._time
	
	@property
	def level(cls):
		from .utils import level_parser
		return level_parser(level=cls._level)
	
	@property
	def team(cls):
		from .utils import get_team
		
		return get_team(cls._get['faction']['id'])
	
class DiscordLeaderboard:
	
	def __init__(self, r):
		self._get = r
		self._time = MayaDT.from_iso8601(r['generated']).datetime()
		self._title = r['generated']
		self._leaderboard = r['leaderboard']
	
	@property
	def title(cls):
		return cls._title
	
	@property
	def time(cls):
		return cls._time
	
	@property
	def top_25(cls):
		return [LeaderboardInstance(x) for x in cls._leaderboard[:25]]
	
	def get_postion(self, postion):
		try:
			return LeaderboardInstance(self._leaderboard[position-1])
		except IndexError:
			warn("{} outside leaderboard length".format(position))
			return None
	
	def get_positions(self, positions):
		return [self.get_postion(x) for x in positions]
	
	@property
	def top(cls):
		return LeaderboardInstance(cls._leaderboard[0])
	
	@property
	def bottom(cls):
		return LeaderboardInstance(cls._leaderboard[-1])
	
	def get_lower_levels(self, min=1, max=39):
		return [LeaderboardInstance(x) for x in self._leaderboard if min <= x['level'] <= max]
	
	@property
	def mystic(cls):
		return cls.filter_teams((1,))
	
	@property
	def valor(cls):
		return cls.filter_teams((2,))
	
	@property
	def instinct(cls):
		return cls.filter_teams((3,))
	
	def filter_teams(self, teams):
		"""Expects an iterable of team IDs"""
		return [LeaderboardInstance(x) for x in self._leaderboard if x['faction']['id'] in teams]
	
	def filter_users(self, users):
		"""Expects an interable of User IDs ints"""
		return [LeaderboardInstance(x) for x in self._leaderboard if x['user_id'] in users]
	
	def filter_trainers(self, trainers):
		"""Expects an interable of Trainer IDs ints"""
		return [LeaderboardInstance(x) for x in self._leaderboard if x['id'] in trainers]
