from typing import TypedDict


class ReadUser(TypedDict):
    id: int
    uuid: str
    username: str
    trainer: int
    
class CreateUser(TypedDict):
    username: str
    