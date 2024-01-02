import databases
import ormar
import sqlalchemy
from enum import Enum
from dotenv import load_dotenv
import os
from insight_backend.models.user import UserRoles
from typing import Optional, List

load_dotenv()

connection_url = os.environ.get("DATABASE_URL")

database = databases.Database(connection_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class UserPendingDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "pending_users"

    id: int = ormar.Integer(primary_key=True)
    telegram_repr: str = ormar.String(max_length=100, unique=True, nullable=False)
    is_username_repr: bool = ormar.Boolean(default=True, nullable=False)
    role: UserRoles = ormar.Enum(enum_class=UserRoles)


class CourseDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "courses"

    id: int = ormar.Integer(primary_key=True)
    course_code: str = ormar.String(max_length=128, nullable=False, unique=True)
    name: str = ormar.String(max_length=600, nullable=False)
    description: str = ormar.String(max_length=1500, nullable=False)


class UserDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    passkey: str = ormar.String(max_length=228, nullable=False)
    telegram_id: str = ormar.String(max_length=100, unique=True, nullable=False)
    telegram_repr: str = ormar.String(max_length=100, unique=True, nullable=False)
    is_username_repr: bool = ormar.Boolean(default=True, nullable=False)
    role: UserRoles = ormar.Enum(enum_class=UserRoles)
    courses: Optional[List[CourseDB]] = ormar.ManyToMany(CourseDB)
