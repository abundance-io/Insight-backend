import databases
import ormar
import sqlalchemy
from enum import Enum
from dotenv import load_dotenv
import os
from .models.user import UserRoles

load_dotenv()

connection_url = os.environ.get("DATABASE_URL")

database = databases.Database(connection_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class UserDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    passkey: str = ormar.String(max_length=228, nullable=False)
    telegram_id: str = ormar.String(max_length=100, unique=True, nullable=False)
    is_username_id: bool = ormar.Boolean(default=True, nullable=False)
    role: UserRoles = ormar.Enum(enum_class=UserRoles)
