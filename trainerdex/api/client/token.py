from typing import ClassVar
from warnings import warn

from trainerdex.api.client.base import BaseClient
from trainerdex.api.http.auth.token import TokenAuth


class TokenClient(BaseClient, TokenAuth):
    _deprecation_message: ClassVar[str] = (
        "TokenClient and the use of TokenAuth will be deprecated in favor of"
        "using the new OAuth2Client and OAuth2Auth classes."
    )

    def __init_subclass__(cls, **kwargs):
        """This throws a deprecation warning on subclassing."""
        warn(cls._deprecation_message, DeprecationWarning, stacklevel=2)
        super().__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        """This throws a deprecation warning on initialization."""
        warn(self._deprecation_message, DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)
