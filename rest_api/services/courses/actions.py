from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Course, CoursePart, PartQuestion, UserCourseProgress, User

from .schemas import CourseInfo


async def get_courses_list(db: Session) -> list[CourseInfo]:
    courses = db.query(Course).all()

    courses_list: list[CourseInfo] = []

    for course in courses:
        courses_list.append(
            CourseInfo.model_validate(course)
        )
    return courses_list


async def get_next_course_part(course_id: int, vk_id: int, db: Session) -> CoursePart:
    user: User | None = db.query(User).filter(vk_id=vk_id).first()

    if user:
        last_passed_part_query = (
            select(CoursePart)
            .join(CoursePart.progress)
            .where(CoursePart.course_id == course_id, UserCourseProgress.user_id == user.id)
        )

        last_passed_part = db.execute(last_passed_part_query).scalars().first()

        course_part_query = (
            select(CoursePart, PartQuestion)
            .join(CoursePart.questions)
            .where(
                CoursePart.course_id == course_id,
                CoursePart.order_number - last_passed_part.order_number == 1
            )
        )

        next_course_part = db.execute(course_part_query).scalars().first()
