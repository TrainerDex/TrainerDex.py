from trainerdex.api.client.base import BaseClient
from trainerdex.api.http.auth.oauth.client_credentials import ClientCredentialsOAuth


class ClientCredentialsClient(BaseClient, ClientCredentialsOAuth):
    pass
