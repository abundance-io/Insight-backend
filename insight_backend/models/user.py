from pydantic import BaseModel
from enum import Enum
from typing import List, Optional


class UserRoles(Enum):
    admin = "admin"
    creator = "creator"
    client = "client"


class UserPending(BaseModel):
    telegram_repr: str
    is_username_repr: bool
    role: UserRoles


class UserCred(BaseModel):
    passkey: str
    telegram_id: str


class User(BaseModel):
    class Config:
        orm_mode = True

    passkey: str
    telegram_id: str
    telegram_repr: str
    is_username_repr: bool
    role: UserRoles


class UserList(BaseModel):
    users: List[User]


class UserPendingList(BaseModel):
    users: List[UserPending]


