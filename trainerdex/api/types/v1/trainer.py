from __future__ import annotations

from typing import List, Optional, TypedDict

from trainerdex.api.types.v1.update import PartialUpdate


class Trainer(TypedDict):
    start_date: str
    faction: int
    trainer_code: str
    last_cheated: Optional[str]
    daily_goal: Optional[int]
    total_goal: Optional[int]
    verified: bool
    statistics: bool


class CreateTrainer(Trainer):
    owner: int


class ReadTrainer(Trainer):
    id: int
    uuid: str
    created_at: str
    updated_at: str
    last_modified: str
    has_cheated: bool
    currently_banned: bool
    owner: int
    username: str
    update_set: List[PartialUpdate]


class EditTrainer(Trainer):
    pass
