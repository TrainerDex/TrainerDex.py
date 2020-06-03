import logging
from typing import Iterable, List

import dateutil.parser

from trainerdex.http import HTTPClient, Route
from trainerdex.models import Trainer, User, Teams

log = logging.getLogger("trainerdex.leaderboard")


class LeaderboardInstance:
    
    def __init__(self, client: HTTPClient = HTTPClient(), **kwargs):
        self.client = client
        self.__kwargs = kwargs
        self.position = kwargs.get('position')
        self._user_id = kwargs.get('user_id')
        self.total_xp = kwargs.get('total_xp')
        self.time = dateutil.parser.parse(kwargs.get('last_updated'))
        self.level = kwargs.get('level')
        self._faction = kwargs.get('faction')
        self._trainer = {
            'id': kwargs.get('id'),
            'username': kwargs.get('username'),
            'faction': kwargs.get('faction').get('id'),
            'owner': kwargs.get('user_id'),
            }
    
    @property
    def trainer(self, detail=False):
        if detail:
            route = Route('GET', '/trainer/{uid}/', uid=self._trainer.get('id'))
            response = self.client.request(route)
            return Trainer(self.client, **response)
        else:
            return Trainer(self.client, **self._trainer)
    
    @property
    def owner(self):
        route = Route('GET', '/users/{uid}', uid=self._user_id)
        response = self.client.request(route)
        return User(self.client, **response)
    
    @property
    def team(self):
        return list(Teams())[self._faction.get('id')]
    
    def __index__(self):
        return self.position-1 # Python Indexes start at 0, but the leaderboard starts at 1
    
    def __bool__(self):
        return True


class BaseLeaderboard:
    
    def __init__(self,  data: List[dict], client: HTTPClient = HTTPClient()):
        self.client = client
        self._data = data
    
    def __iter__(self):
        for x in self._data:
            yield LeaderboardInstance(self.client, **x)
    
    def __reversed__(self):
        for x in reversed(self._data):
            yield LeaderboardInstance(self.client, **x)
    
    def __len__(self):
        return len(self._data)
    
    def get_postion(self, position: int) -> LeaderboardInstance:
        return self.__getitem__(position-1)
    
    def get_positions(self, positions: Iterable[int]):
        for x in positions:
            yield self.get_postion(x)
    
    def __getitem__(self, key) -> LeaderboardInstance:
        return LeaderboardInstance(self.client, **self._data[key])
    
    def __contains__(self, item: Trainer) -> bool:
        return bool([x for x in self._data if x.get('id') == item.id])
    
    @property
    def top(self):
        return self.get_postion(1)
    
    @property
    def bottom(self):
        return self.get_postion(0)
    
    def filter_levels(self, min: int = 1, max: int = 40):
        for x in self._data:
            if min <= x.get('level') <= max:
                yield LeaderboardInstance(self.client, **x)
    
    @property
    def mystic(self):
        return self.filter_teams({1})
    
    @property
    def valor(self):
        return self.filter_teams({2})
    
    @property
    def instinct(self):
        return self.filter_teams({3})
    
    def filter_teams(self, teams: Iterable[int]):
        for x in self._data:
            if x.get('faction').get('id') in teams:
                yield LeaderboardInstance(self.client, **x)
    
    def filter_users(self, users: Iterable[int]):
        for x in self._data:
            if x.get('user_id') in users:
                yield LeaderboardInstance(self.client, **x)
    
    def filter_trainers(self, trainers: Iterable[int]):
        for x in self._data:
            if x.get('id') in trainers:
                yield LeaderboardInstance(self.client, **x)


class WorldwideLeaderboard(BaseLeaderboard):
    pass


class DiscordLeaderboard(BaseLeaderboard):
    
    def __init__(self, data: List[dict], client: HTTPClient = HTTPClient()):
        self.client = client
        self.time = dateutil.parser.parse(data.get('generated'))
        self.title = data.get('title')
        self._data = data.get('leaderboard')
