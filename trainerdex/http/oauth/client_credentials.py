import base64
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import NoReturn
from zoneinfo import ZoneInfo

from aiohttp import ClientResponseError
from promise import promisify
from trainerdex.exceptions.auth import AuthenticationError

from trainerdex.http.oauth.interface import iOAuthClient


@dataclass
class ClientCredentialsToken:
    access_token: str
    expires_in: int
    expires_at: datetime
    token_type: str
    scope: str

    def __repr__(self) -> str:
        return super().__str__().replace(self.access_token, "*" * len(self.access_token))


class OAuthCredentialsClient(iOAuthClient):
    token: ClientCredentialsToken = None

    def __repr__(self) -> str:
        if self.token is None:
            return "OAuthCredentialsClient()"
        else:
            return f"OAuthCredentialsClient(token={self.token})"

    def __str__(self) -> str:
        if self.token is None:
            return "<OAuthCredentialsClient: No token>"
        else:
            return (
                f"<OAuthCredentialsClient: Token expires at {self.token.expires_at.isoformat()}>"
            )

    @promisify
    async def __del__(self) -> None:
        await self.session.close()

    def encode_credentials(self, client_id: str, client_secret: str) -> str:
        return base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")

    async def authenticate(
        self, client_id: str, client_secret: str, *args, **kwargs
    ) -> bool | NoReturn:
        path = "/api/oauth/token/"
        credentials = self.encode_credentials(client_id, client_secret)

        headers = {
            "Authorization": f"Basic {credentials}",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "client_credentials",
        }

        async with self.session.post(path, headers=headers, data=data) as resp:
            response_datetime = datetime.utcnow().astimezone(tz=ZoneInfo("UTC"))
            try:
                resp.raise_for_status()
            except ClientResponseError as e:
                raise AuthenticationError() from e
            response = await resp.json()
            self.token = ClientCredentialsToken(
                expires_at=response_datetime + timedelta(seconds=response["expires_in"]),
                **response,
            )

            self.session.headers["Authorization"] = f"Bearer {self.token.access_token}"

        return await self.test_authentication()

    async def test_authentication(self) -> bool:
        path = "/api/oauth/test/"
        async with self.session.get(path) as resp:
            return resp.ok
