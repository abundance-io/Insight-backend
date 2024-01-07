from pydantic import BaseModel
from typing import List,Dict
from enum import Enum


class Course(BaseModel):
    course_code: str
    name: str
    description: str


class CourseList(BaseModel):
    courses: List[Course]


class ContentType(Enum):
    section = "section"
    quiz = "quiz"
    note_summary = "note_summary"
    flashcard = "flashcard"
