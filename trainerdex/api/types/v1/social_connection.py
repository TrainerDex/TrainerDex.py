from __future__ import annotations

from typing import Dict, Optional, TypedDict


class SocialConnection(TypedDict):
    user: int
    provier: str
    uid: str
    extra_data: Optional[Dict]


class ReadSocialConnection(SocialConnection):
    trainer: int


class CreateSocialConnection(SocialConnection):
    pass
