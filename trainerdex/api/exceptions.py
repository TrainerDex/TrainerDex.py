from aiohttp import ClientResponseError


class HTTPException(ClientResponseError):
    pass


class Forbidden(ClientResponseError):
    pass


class NotFound(ClientResponseError):
    pass
