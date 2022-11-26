import base64
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import ClassVar, Optional
from zoneinfo import ZoneInfo

from typing_extensions import Self

from trainerdex.api.http.base import BaseHTTPClient


@dataclass(frozen=True, slots=True)
class ClientCredentialsToken:
    access_token: str
    expires_in: int
    expires_at: datetime
    token_type: str
    scope: str

    def __repr__(self) -> str:
        return super().__str__().replace(self.access_token, "*" * len(self.access_token))


class ClientCredentialsOAuth(BaseHTTPClient):
    TOKEN_AUTH_URL: ClassVar[str] = "/api/oauth/token/"
    _token: Optional[ClientCredentialsToken]

    async def authenticate(self, *, client_id: str, client_secret: str) -> Self:
        credentials = self._encode_credentials(client_id=client_id, client_secret=client_secret)

        headers = {
            "Authorization": f"Basic {credentials}",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
        }

        async with self.session.post(self.TOKEN_AUTH_URL, headers=headers, data=data) as resp:
            response_datetime = datetime.utcnow().astimezone(tz=ZoneInfo("UTC"))
            resp.raise_for_status()
            response = await resp.json()
            self._token = ClientCredentialsToken(
                expires_at=response_datetime + timedelta(seconds=response["expires_in"]),
                **response,
            )

            self.session.headers["Authorization"] = f"Bearer {self._token.access_token}"
            if await self._test_authentication():
                self._authenticated = True

        return self

    def _encode_credentials(self, *, client_id: str, client_secret: str) -> str:
        return base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")

    async def _test_authentication(self) -> bool:
        path = "/api/oauth/test/"
        async with self.session.get(path) as resp:
            return resp.ok
