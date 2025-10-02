from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Course, CoursePart, PartQuestion, UserCourseProgress, User, UserCourseFeedback
from db.utils import get_user_by_vk_id
from schemas import BaseResponse

from .schemas import CourseInfo, CoursePart as CoursePartSchema, CoursePartQuestionAnswer, CourseFeedback


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
            .order_by(UserCourseProgress.date.desc())
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
                .join(PartQuestion, PartQuestion.part_id == CoursePart.id)
                .where(
                    CoursePart.course_id == course_id,
                    CoursePart.order_number == 1
                )
            )

        course_part_data = db.execute(course_part_query).first()

        course_part = CoursePartSchema(
            id=course_part_data[0].id,
            title=course_part_data[0].title,
            description=course_part_data[0].description,
            video_url=course_part_data[0].video_url,
            image_url=course_part_data[0].image_url,
            last_part=course_part_data[0].last_part,
            question_id=course_part_data[1].id,
            question=course_part_data[1].question,
            answer_1=course_part_data[1].answer_1,
            answer_2=course_part_data[1].answer_2,
            answer_3=course_part_data[1].answer_3,
            answer_4=course_part_data[1].answer_4,
            correct_answer=course_part_data[1].correct_answer,
            correct_message=course_part_data[1].correct_message,
            incorrect_message=course_part_data[1].incorrect_message
        )

        return course_part

    raise Exception(f"User with vk_id={vk_id} not found")


async def get_part_by_id(course_id: int, part_id: int, db: Session) -> CoursePartSchema:
    course_part_query = (
        select(CoursePart, PartQuestion)
        .join(PartQuestion, PartQuestion.part_id == CoursePart.id)
        .where(
            CoursePart.course_id == course_id,
            CoursePart.id == part_id
        )
    )

    course_part_data = db.execute(course_part_query).first()

    course_part = CoursePartSchema(
        id=course_part_data[0].id,
        title=course_part_data[0].title,
        description=course_part_data[0].description,
        video_url=course_part_data[0].video_url,
        image_url=course_part_data[0].image_url,
        last_part=course_part_data[0].last_part,
        question_id=course_part_data[1].id,
        question=course_part_data[1].question,
        answer_1=course_part_data[1].answer_1,
        answer_2=course_part_data[1].answer_2,
        answer_3=course_part_data[1].answer_3,
        answer_4=course_part_data[1].answer_4,
        correct_answer=course_part_data[1].correct_answer,
        correct_message=course_part_data[1].correct_message,
        incorrect_message=course_part_data[1].incorrect_message
    )

    return course_part


async def save_answer(answer: CoursePartQuestionAnswer, db: Session):
    user = get_user_by_vk_id(db, answer.vk_id)

    progress = UserCourseProgress(
        user=user,
        part_id=answer.part_id,
        part_question_id=answer.part_question_id,
        answer=answer.answer
    )

    db.add(progress)
    db.commit()
    db.flush()

    return BaseResponse(success=True, message="Прогресс сохранён")


async def save_course_feedback(feedback: CourseFeedback, db: Session):
    user = get_user_by_vk_id(db, feedback.vk_id)

    feedback_to_save = UserCourseFeedback(
        user=user,
        course_id=feedback.course_id,
        rate=feedback.rate,
        rate_description=feedback.rate_description,
        public_feedback=feedback.public_feedback
    )

    db.add(feedback_to_save)
    db.commit()

    return BaseResponse(success=True, message="Отзыв записан")
