from typing_extensions import Self

from trainerdex.api.http.base import BaseHTTPClient


class TokenAuth(BaseHTTPClient):
    def authenticate(self, *, token: str) -> Self:
        self._headers["Authorization"] = f"Token {token}"
        self._authenticated = True
        return self
