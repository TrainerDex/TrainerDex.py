# from .client import Client


class User:
    """Represents a user"""
    
    def __init__(self, r):
        self._get = r
        self.id = r['id']
        self.username = r['username']
        self.first_name = r['first_name']
        self.last_name = r['last_name']
        self.profiles = r['profiles']
    
    def trainer(self):
        trainers = []
        for x in self.profiles:
            trainers.append(Client().get_trainer(x))
        return trainers
    
    def discord(self):
        return Client().get_discord_user(user=[str(self.id)])
    
    def __hash__(self):
        return self.id
    
    def __eq__(self, other):
        return self.id == other.id
