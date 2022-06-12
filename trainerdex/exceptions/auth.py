from aiohttp import ClientResponseError


class AuthenticationError(ClientResponseError):
    pass
