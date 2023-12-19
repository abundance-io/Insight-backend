from pydantic import BaseModel
from typing import List


class Course(BaseModel):
    course_code: str
    name: str
    description: str


class CourseList(BaseModel):
    courses: List[Course]
