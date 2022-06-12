from abc import abstractmethod
from trainerdex.http.interface import iHTTPClient


class iOAuthClient(iHTTPClient):
    @abstractmethod()
    def authenticate(self, client_id: str, client_secret: str, *args, **kwargs):
        ...
