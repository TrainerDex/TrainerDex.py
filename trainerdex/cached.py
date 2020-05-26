from json import loads

from trainerdex.models import User
from trainerdex.http import HTTPClient, Route

class DiscordUser:
    """Represents a cached Discord user"""
    
    def __init__(self, client: HTTPClient = HTTPClient(), **kwargs):
        self.client = client
        self.__kwargs = kwargs
        self.__user = kwargs.get('user')
        self.provider = kwargs.get('provider')
        self.uid = kwargs.get('uid')
        self.extra_data = loads(kwargs.get('extra_data', '{}').replace("True", "true").replace("False", "false"))
        
    @property
    def username(self):
        return self.extra_data.get('username')
    
    @property
    def discriminator(self):
        return self.extra_data.get('discriminator')
    
    def __str__(self):
        if self.username and self.discriminator:
            return "{}#{}".format(self.username, self.discriminator)
    
    def __repr__(self):
        return "DiscordUser(**{})".format(self.__kwargs)
    
    @property
    def owner(self):
        route = Route('GET', '/users/{uid}', uid=self.__owner)
        response = self.client.request(route)
        return User(self.client, **response)
