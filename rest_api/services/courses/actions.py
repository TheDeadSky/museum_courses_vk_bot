from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Course, CoursePart, PartQuestion, UserCourseProgress, User

from .schemas import CourseInfo, CoursePart as CoursePartSchema


async def get_courses_list(db: Session) -> list[CourseInfo]:
    courses = db.query(Course).all()

    courses_list: list[CourseInfo] = []

    for course in courses:
        courses_list.append(
            CourseInfo.model_validate(course)
        )
    return courses_list


async def get_course(course_id: int, db: Session) -> CourseInfo:
    course = db.query(Course).filter(Course.id == course_id).first()

    if course is None:
        raise Exception(f"Course {course_id} not found")

    return CourseInfo.model_validate(course)


async def get_next_course_part(course_id: int, vk_id: int, db: Session) -> CoursePartSchema:
    user: User | None = db.query(User).filter(User.vk_id == vk_id).first()

    if user:
        last_passed_part_query = (
            select(CoursePart)
            .join(CoursePart.progress)
            .where(CoursePart.course_id == course_id, UserCourseProgress.user_id == user.id)
        )

        last_passed_part = db.execute(last_passed_part_query).scalars().first()

        if last_passed_part:
            next_part_number = last_passed_part.order_number + 1
            course_part_query = (
                select(CoursePart, PartQuestion)
                .join(CoursePart.questions)
                .where(
                    CoursePart.course_id == course_id,
                    CoursePart.order_number == next_part_number
                )
            )
        else:
            course_part_query = (
                select(CoursePart, PartQuestion)
                .join(CoursePart.questions)
                .where(
                    CoursePart.course_id == course_id,
                    CoursePart.order_number == 1
                )
            )

        next_course_part = db.execute(course_part_query).scalars().first()

        course_part = CoursePartSchema.model_validate(next_course_part)

        return course_part

    raise Exception(f"User with vk_id={vk_id} not found")


async def get_part_by_id(course_id: int, part_id: int, db: Session) -> CoursePartSchema:
    course_part_query = (
        select(CoursePart, PartQuestion)
        .join(CoursePart.questions)
        .where(
            CoursePart.course_id == course_id,
            CoursePart.id == part_id
        )
    )

    course_part = db.execute(course_part_query).scalars().first()

    return course_part
