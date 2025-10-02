from constants import COURSES_LIST_KEY
from models.courses import CourseInfo, CoursePart, CoursePartQuestionAnswer
from services.entities.base import AbstractEntityService


class CoursesService(AbstractEntityService):
    module = "courses"

    async def list(self) -> list[CourseInfo] | None:
        courses = []
        courses_raw: list = self._cache_service.get(COURSES_LIST_KEY)

        if courses_raw is None:
            try:
                courses_raw = await self._api_service.read(
                    module=self.module
                )

                self._cache_service.update(COURSES_LIST_KEY, courses_raw, 300)

            except Exception as e:
                print(f"CoursesServiceError: {e}")
                return None

        for course in courses_raw:
            courses.append(CourseInfo(**course))

        return courses

    async def get_course(self, course_id: int) -> CourseInfo | None:
        course_key = f"course_{course_id}"
        course: CourseInfo
        course_raw: dict = self._cache_service.get(course_key)

        if course_raw is None:
            try:
                course_raw = await self._api_service.read(
                    module=f"{self.module}/{course_id}",
                )

                self._cache_service.update(course_key, course_raw)

            except Exception as e:
                print(f"CoursesServiceError: {e}")
                return None

        course = CourseInfo(**course_raw)

        return course

    async def get_part(self, course_id: int, course_part_id: int) -> CoursePart | None:
        course_part_key = f"course_part_{course_part_id}"
        course_part: CoursePart
        course_part_raw: dict = self._cache_service.get(course_part_key)

        if course_part_raw is None:
            try:
                course_part_raw = await self._api_service.read(
                    module=f"{self.module}/{course_id}/parts/{course_part_id}",
                )

                self._cache_service.update(course_part_key, course_part_raw)

            except Exception as e:
                print(f"CoursesServiceError: {e}")
                return None

        course = CoursePart(**course_part_raw)

        return course

    async def get_next_part(self, vk_id: int, course_id: int) -> CoursePart | None:
        part_module = f"{self.module}/{course_id}/parts/next"
        try:
            response = await self._api_service.read(
                module=part_module,
                data={
                    "vk_id": vk_id
                }
            )

            return CoursePart(**response)

        except Exception as e:
            print(f"CoursesServiceError for '{vk_id}': {e}")
            return None

    async def send_answer(self, answer: CoursePartQuestionAnswer) -> bool:
        part_module = f"{self.module}/{answer.course_id}/parts/{answer.part_id}"
        try:
            await self._api_service.create(
                module=part_module,
                data={
                    "vk_id": answer.vk_id,
                    "part_question_id": answer.part_question_id,
                    "answer": answer.answer,
                }
            )

            return True

        except Exception as e:
            print(f"CoursesServiceError for '{answer.vk_id}': {e}")
            return False
