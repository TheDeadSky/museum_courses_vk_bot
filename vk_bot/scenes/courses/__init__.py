from vkbottle.bot import BotLabeler
from ._01_enter import courses_enter_labeler
from ._02_start_course import course_labeler
from ._03_question import course_question_labeler
from ._04_rate_course import course_feedback_labeler

courses_labeler = BotLabeler()

courses_labeler.load(courses_enter_labeler)
courses_labeler.load(course_labeler)
courses_labeler.load(course_question_labeler)
courses_labeler.load(course_feedback_labeler)

__all__ = ["courses_labeler"]
