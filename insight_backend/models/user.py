from pydantic import BaseModel
from enum import Enum


class UserRoles(Enum):
    admin = "admin"
    creator = "creator"
    client = "client"


class UserCred(BaseModel):
    passkey: str
    telegram_id: str


class User(BaseModel):
    class Config:
        orm_mode = True

    passkey: str
    telegram_id: str
    is_username_id: bool
    role: UserRoles
