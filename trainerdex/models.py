from json import load, loads
import logging
import os
import re
import uuid

import dateutil.parser

from trainerdex.http import HTTPClient, Route

log = logging.getLogger("trainerdex.models")

LEVELS_JSON_PATH = os.path.join(os.path.dirname(__file__), 'data/levels.json')
FACTIONS_JSON_PATH = os.path.join(os.path.dirname(__file__), 'data/factions.json')


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
    
    @property
    def discords(self):
        route = Route('GET', '/users/social')
        parameters = {
            'provider': 'discord',
            'user': self.id,
        }
        response = self.client.request(route, params=parameters)
        for x in response:
            yield DiscordUser(self.client, **x)
    
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
        """Iterate over the Updates, sorted newest first"""
        for x in sorted(self.__update_set, key=lambda x: dateutil.parser.parse(x.get('update_time')), reverse=True):
            yield Update(self.client, **x)
    
    @property
    def team(self):
        return list(Teams())[self._faction]
    
    @property
    def owner(self):
        route = Route('GET', '/users/{uid}', uid=self.__owner)
        response = self.client.request(route)
        return User(self.client, **response)
    
    def get_current_stat(self, stat):
        """Gets the latest of the provided stat"""
        for x in self.updates:
            if getattr(x, stat) is not None:
                return getattr(x, stat)
    
    @property
    def level(self):
        for x in reversed(list(Levels())):
            qualifying_factors = 0
            
            if x.requirements is None:
                # If there are no requirements to reach that level, we assume it's that level
                # Aka, level 1
                return x
            
            for stat, value in x.requirements.items():
                if self.get_current_stat(stat) >= value:
                    qualifying_factors += 1
            
            if qualifying_factors == len(x.requirements):
                return x


class Update:
    """Represents an Basic Update object on the API"""
    
    def __init__(self, client: HTTPClient = HTTPClient(), **kwargs):
        self.client = client
        self.__kwargs = kwargs
        self.uuid = uuid.UUID(hex=kwargs.get('uuid'))
        self.__trainer = kwargs.get('trainer')
        self.update_time = dateutil.parser.parse(kwargs.get('update_time'))
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
        return None
    
    def __repr__(self):
        return "Update(**{})".format(self.__kwargs)
    
    @property
    def level(self):
        for x in reversed(list(Levels())):
            qualifying_factors = 0
            
            if x.requirements is None:
                # If there are no requirements to reach that level, we assume it's that level
                # Aka, level 1
                return x
            
            for stat, value in x.requirements.items():
                if getattr(self, stat) >= value:
                    qualifying_factors += 1
            
            if qualifying_factors == len(x.requirements):
                return x
    
    @property
    def trainer(self) -> Trainer:
        route = Route('GET', '/trainers/{uid}/', uid=self.__trainer)
        response = self.client.request(route)
        return Trainer(self.client, **response)


class Level:
    # This model doesn't need to call the API
    
    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.level = kwargs.get('level')
        # set requirements up to accept a dict of values, incase Niantic ever decide to add further levels with badge requirements such as in Ingress
        self.requirements = kwargs.get('requirements') # dict: {'total_xp': 0}
        self.rewards = kwargs.get('rewards')
        self.unlocks = kwargs.get('unlocks')
    
    def __str__(self):
        return "Level {}".format(self.level)
    
    def __repr__(self):
        return "Level(**{})".format(self.__kwargs)
    
    def __index__(self):
        return self.level
    
    def __next__(self):
        with open(LEVELS_JSON_PATH) as file:
            levels = load(file)
            next_level = levels.get(self.index+1)
            if next_level:
                return self.__class__(**next_level)
            else:
                raise StopIteration
    
    @property
    def requirements_to_complete(self):
        """Returns the requirements to reach the next level. Useful for progress bars and such!
        
        Returns None if end level (Level 40)
        """
        try:
            return next(self).requirements
        except StopIteration:
            return None

def Levels():
    with open(LEVELS_JSON_PATH) as file:
        levels = load(file)
        for x in levels:
            if x:
                yield Level(**x)
            else:
                yield x


class Team:
    
    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.name = kwargs.get('name')
        self.color = kwargs.get('color')
        self.colour = self.color
        self.leader = kwargs.get('leader')
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "Team(**{})".format(self.__kwargs)
    
    def __index__(self):
        return self.__kwargs.get('faction')
    
    def __next__(self):
        with open(FACTIONS_JSON_PATH) as file:
            factions = load(file)
            try:
                return self.__class__(**factions[self.__index__()+1])
            except IndexError:
                raise StopIteration
    
    def hex(self) -> str:
        """Returns the hex as a string"""
        if self.color:
            return "#{0:06X}".format(self.color.get('hex'))

def Teams():
    with open(FACTIONS_JSON_PATH) as file:
        factions = load(file)
        for x in factions:
            yield Team(**x)


class DiscordUser:
    """Represents a weak-representation of a Discord user
    
    Parameters
    """
    
    def __init__(self, client: HTTPClient = HTTPClient(), **kwargs):
        self.client = client
        self.__kwargs = kwargs
        self.__user = kwargs.get('user')
        self.__provider = kwargs.get('provider')
        self.__uid = kwargs.get('uid')
        self.__extra_data = loads(kwargs.get('extra_data', '{}').replace("'", '"').replace("True", "true").replace("False", "false"))
        
    def __getattr__(self, name):
        return self.__extra_data.get(name)
    
    def __str__(self):
        if self.username and self.discriminator:
            return "{}#{}".format(self.username, self.discriminator)
        return self.__repr__
    
    def __repr__(self):
        return "DiscordUser(**{})".format(self.__kwargs)
    
    @property
    def owner(self):
        route = Route('GET', '/users/{uid}', uid=self.__owner)
        response = self.client.request(route)
        return User(self.client, **response)
