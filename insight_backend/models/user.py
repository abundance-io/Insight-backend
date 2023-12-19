from pydantic import BaseModel
from enum import Enum
from typing import List, Optional


class UserRoles(Enum):
    admin = "admin"
    creator = "creator"
    client = "client"


class UserCred(BaseModel):
    passkey: str
    telegram_id: str


class UserBase(BaseModel):
    telegram_id: str


class User(BaseModel):
    class Config:
        orm_mode = True

    passkey: str
    telegram_id: str
    is_username_id: bool
    role: UserRoles


class UserList(BaseModel):
    users: List[User]
