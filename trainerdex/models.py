import re
import uuid

import dateutil.parser

from trainerdex.cached import DiscordUser
from trainerdex.http import HTTPClient, Route
from trainerdex.utils import get_team, level_parser


class User:
    """Represents a user"""
    
    def __init__(self, client: HTTPClient = HTTPClient(), **kwargs):
        self.client = client
        self.__kwargs = kwargs
        self.id = kwargs.get('id')
        self.username = kwargs.get('username')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.__trainer = kwargs.get('trainer')
    
    @property
    def trainer(self):
        route = Route('GET', '/trainers/{uid}/', uid=self.__trainer)
        response = self.client.request(route)
        return Trainer(self.client, **response)
    
    def discords(self):
        route = Route('GET', '/users/social')
        parameters = {
            'provider': 'discord',
            'user': self.id,
        }
        response = self.client.request(route, params=parameters)
        for x in response:
            yield DiscordUser(x)
    
    def __hash__(self):
        return self.id
    
    def __repr__(self):
        return "User(**{})".format(self.__kwargs)
    
    def __eq__(self, other):
        return self.id == other.id


class Trainer:
    """Represents a Trainer Profile"""
    
    def __init__(self, client: HTTPClient = HTTPClient(), **kwargs):
        self.client = client
        self.__kwargs = kwargs
        self.id = kwargs.get('id')
        self.last_modified = dateutil.parser.parse(kwargs.get('last_modified'))
        self.__owner = kwargs.get('owner')
        self.username = kwargs.get('username')
        self.nickname = self.username
        try:
            self.start_date = dateutil.parser.parse(kwargs.get('start_date'))
        except TypeError:
            self.start_date = None
        self._faction = kwargs.get('faction')
        self.trainer_code = re.sub(r'\D', '', kwargs.get('trainer_code'))
        self.has_cheated = kwargs.get('has_cheated')
        self.legit = not self.has_cheated
        try:
            self.last_cheated = dateutil.parser.parse(kwargs.get('last_cheated'))
        except TypeError:
            self.last_cheated = None
        self.daily_goal = kwargs.get('daily_goal')
        self.total_goal = kwargs.get('total_goal')
        self.__update_set = kwargs.get('update_set')
        self.verified = kwargs.get('verified')
        
    def __str__(self):
        return self.username
    
    def __repr__(self):
        return "Trainer(**{})".format(self.__kwargs)
    
    def __hash__(self):
        return self.id
    
    def __eq__(self, other):
        return self.id == other.id
    
    @property
    def updates(self):
        for x in sorted(self.__update_set, key=lambda x: dateutil.parser.parse(x.get('update_time'))):
            yield Update(self.client, **x)
    
    @property
    def team(self):
        return get_team(self._faction)
    
    @property
    def owner(self):
        route = Route('GET', '/users/{uid}', uid=self.__owner)
        response = self.client.request(route)
        return User(self.client, **response)


class Update:
    """Represents an Basic Update object on the API"""
    
    def __init__(self, client: HTTPClient = HTTPClient(), **kwargs):
        self.client = client
        self.__kwargs = kwargs
        self.uuid = uuid.UUID(hex=kwargs.get('uuid'))
        self.__trainer = kwargs.get('trainer')
        self._modified_extra_fields = kwargs.get('modified_extra_fields')

    def refresh(self):
        route = Route('GET', '/trainers/{trainer}/updates/{update}/', trainer=self.__trainer, update=self.uuid.hex)
        response = self.client.request(route)
        self.__kwargs.update(response)
    
    def __getattr__(self, name):
        if self.__kwargs.get(name) is not None:
            return self.__kwargs.get(name)
        elif name in self._modified_extra_fields+['data_source', 'total_xp']:
            self.refresh()
            return self.__kwargs.get(name)
    
    def __repr__(self):
        return "Update(**{})".format(self.__kwargs)
    
    @property
    def level(self):
        return level_parser(xp=self.total_xp)
    
    @property
    def trainer(self) -> Trainer:
        route = Route('GET', '/trainers/{uid}/', uid=self.__trainer)
        response = self.client.request(route)
        return Trainer(self.client, **response)
