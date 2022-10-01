from trainerdex.api.client.base import BaseClient
from trainerdex.api.http.auth.token import TokenAuth


class TokenClient(BaseClient, TokenAuth):
    pass
