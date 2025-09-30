import logging

from models.courses import CourseInfo, CoursePart, CoursePartQuestionAnswer
from services.entities.base import AbstractEntityService


class CoursesService(AbstractEntityService):
    module = "courses"

    async def list(self) -> list[CourseInfo] | None:
        try:
            response = await self.api_service.read(
                module=self.module
            )

            courses = []
            for course in response:
                courses.append(CourseInfo(**course))

            return courses

        except Exception as e:
            logging.error(f"CoursesServiceError: {e}")
            return None

    async def get_next_part(self, vk_id: int, course_id: int) -> CoursePart | None:
        part_module = f"{self.module}/{course_id}/parts/next/"
        try:
            response = await self.api_service.read(
                module=part_module,
                data={
                    "vk_id": vk_id
                }
            )

            return CoursePart(**response)

        except Exception as e:
            logging.error(f"CoursesServiceError for '{vk_id}': {e}")
            return None

    async def send_answer(self, answer: CoursePartQuestionAnswer) -> bool:
        part_module = f"{self.module}/{answer.course_id}/parts/{answer.part_id}/"
        try:
            await self.api_service.create(
                module=part_module,
                data={
                    "vk_id": answer.vk_id,
                    "part_question_id": answer.part_question_id,
                    "answer": answer,
                }
            )

            return True

        except Exception as e:
            logging.error(f"CoursesServiceError for '{answer.vk_id}': {e}")
            return False
