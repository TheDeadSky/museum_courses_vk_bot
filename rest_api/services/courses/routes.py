from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from schemas import BaseResponse
from .actions import get_courses_list, get_next_course_part, get_part_by_id, get_course, save_answer, \
    save_course_feedback
from .schemas import CourseInfo, CoursePart, CoursePartQuestionAnswer, CourseFeedback

router = APIRouter()


@router.get("/courses/")
async def courses_list(db: Session = Depends(get_db)) -> list[CourseInfo]:
    """Get a self-support course for a user"""
    return await get_courses_list(db)


@router.get("/courses/{course_id}/")
async def course(course_id: int, db: Session = Depends(get_db)) -> CourseInfo:
    """Get a self-support course for a user"""
    return await get_course(course_id, db)


@router.get("/courses/{course_id}/parts/next/")
async def next_course_part(course_id: int, vk_id: int, db: Session = Depends(get_db)) -> CoursePart:
    return await get_next_course_part(course_id, vk_id, db)


@router.get("/courses/{course_id}/parts/{part_id}/")
async def next_course_part(course_id: int, part_id: int, db: Session = Depends(get_db)) -> CoursePart:
    return await get_part_by_id(course_id, part_id, db)


@router.post("/courses/{course_id}/parts/{part_id}/")
async def next_course_part(answer: CoursePartQuestionAnswer, db: Session = Depends(get_db)) -> BaseResponse:
    return await save_answer(answer, db)


@router.post("/courses/{course_id}/feedback/")
async def course_feedback(feedback: CourseFeedback, db: Session = Depends(get_db)) -> BaseResponse:
    return await save_course_feedback(feedback, db)
