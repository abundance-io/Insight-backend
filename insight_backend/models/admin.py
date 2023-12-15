import ormar
from ..db import BaseMeta
from pydantic import BaseModel


class AdminDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "admins"

    id: int = ormar.Integer(primary_key=True)
    passkey: str = ormar.String(max_length=228, nullable=False)
    telegram_id: str = ormar.String(max_length=100, unique=True, nullable=False)
    is_username_id: bool = ormar.Boolean(default=True, nullable=False)


class Admin(BaseModel):
    class Config:
        orm_mode = True

    passkey: str
    telegram_id: str
    is_username_id: bool
