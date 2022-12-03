from typing import Literal, TypedDict


class ReadDiscordConfig(TypedDict):
    id: int
    name: str
    language: str
    timezone: str
    assign_roles_on_join: bool
    set_nickname_on_join: bool
    set_nickname_on_update: bool
    level_format: Literal["none", "int", "circled_level"]
    weekly_leaderboards_enabled: bool
    mystic_role: int
    valor_role: int
    instinct_role: int
    tl40_role: int
    tl50_role: int
    leaderboard_channel: int
    roles_to_append_on_approval: list[int]
    roles_to_remove_on_approval: list[int]
    mod_role_ids: list[int]
