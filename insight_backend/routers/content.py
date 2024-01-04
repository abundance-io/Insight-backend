from fastapi import APIRouter
from ..db import CourseDB
from ormar.exceptions import NoMatch
from fastapi import APIRouter, Depends
from ..models.content import Course, CourseList
from fastapi import HTTPException


course_router = APIRouter()
router = course_router


@router.get("/course/{course_code}")
async def get_course(course_code: str):
    if course_code != "all":
        course_code = course_code.lower().replace(" ", "")
        try:
            course = await CourseDB.objects.get(course_code=course_code)
            return Course(**course.dict())
        except NoMatch:
            raise HTTPException(detail="course does not exist", status_code=404)
    else:
        courses = await CourseDB.objects.all()
        return CourseList(**{"courses": courses})
