class ValidationError(ValueError):
    pass


class HTTPException(Exception):
    pass


class Forbidden(Exception):
    pass


class NotFound(Exception):
    pass
