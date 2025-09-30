from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from .actions import get_courses_list, get_next_course_part
from .schemas import CourseInfo, CoursePart

router = APIRouter()


@router.post("/courses/")
async def courses_list(db: Session = Depends(get_db)) -> list[CourseInfo]:
    """Get a self-support course for a user"""
    return await get_courses_list(db)


@router.get("/courses/{course_id}/part/next")
async def next_course_part(course_id: int, vk_id: int, db: Session = Depends(get_db)) -> CoursePart:
    return await get_next_course_part(course_id, vk_id, db)