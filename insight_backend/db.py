from typing import Union, Dict
import databases
import ormar
import sqlalchemy
from enum import Enum
from dotenv import load_dotenv
import os
from insight_backend.models.user import UserRoles
from insight_backend.models.content import ContentType
from typing import Optional, List

load_dotenv()


#todo! make the creator profile thing not suck
connection_url = os.environ.get("DATABASE_URL")
if not connection_url:
    raise Exception("database not supplied")


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


class DepartmentDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "departments"
        name: str = ormar.String(
            max_length=500, nullable=False, primary_key=True, unique=True
        )


class UserDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    passkey: str = ormar.String(max_length=228, nullable=False)
    telegram_id: str = ormar.String(max_length=100, unique=True, nullable=False)
    telegram_repr: str = ormar.String(max_length=100, unique=True, nullable=False)
    is_username_repr: bool = ormar.Boolean(default=True, nullable=False)
    role: UserRoles = ormar.Enum(enum_class=UserRoles)


class CreatorsDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "creators"

    id: int = ormar.Integer(primary_key=True)
    user: Optional[Union[UserDB, Dict]] = ormar.ForeignKey(
        UserDB, related_name="creator_profile"
    )


class CourseDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "courses"

    course_code: str = ormar.String(
        max_length=100, nullable=False, primary_key=True, unique=True
    )
    name: str = ormar.String(max_length=500, nullable=False, unique=True)
    description:str = ormar.Text();
    department: Optional[Union[DepartmentDB, Dict]] = ormar.ForeignKey(DepartmentDB)
    creators: Optional[List[CreatorsDB]] = ormar.ManyToMany(CreatorsDB,related_name="courses")


class SectionDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "sections"

    id: int = ormar.Integer(primary_key=True)


class ContentDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "content"

    id: int = ormar.Integer(primary_key=True)
    reference_id: int = ormar.Integer()
    content_type: ContentType = ormar.Enum(enum_class=ContentType)
    course: Optional[Union[CourseDB, Dict]] = ormar.ForeignKey(CourseDB)
    section: Optional[Union[DepartmentDB, Dict]] = ormar.ForeignKey(DepartmentDB)


class QuizDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "quizzes"

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=500, nullable=False, unique=True)


class QuestionDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "questions"

    id: int = ormar.Integer(primary_key=True)
    question: str = ormar.Text()
    options: str = ormar.Text()
    correct: str = ormar.String(max_length=1)
    quiz: Optional[Union[QuizDB, Dict]] = ormar.ForeignKey(QuizDB)


class FlashCardDB(ormar.Model):
    class Meta(BaseMeta):
        tablename = "flashcards"

    id: int = ormar.Integer(primary_key=True)
    front: str = ormar.Text()
    back: str = ormar.Text()
