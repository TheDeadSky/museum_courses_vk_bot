from vkbottle.bot import BotLabeler, MessageEvent

from actions.general import make_rating_menu
from customs.events import callback_handler
from menus import TO_MAIN_MENU_BUTTON
from models.courses import CoursePart, CourseInfo, CoursePartQuestionAnswer
from settings import services
from utils import make_one_button_menu, merge_inline_menus

course_question_labeler = BotLabeler()


@callback_handler(course_question_labeler, cmd="answer_question")
async def start_course(event: MessageEvent):
    event_payload = event.payload
    course = CourseInfo(**event_payload["course"])
    course_part = CoursePart(**event_payload["course_part"])
    answer = event_payload["answer_id"]
    correct_answer_id = event_payload["correct_answer_id"]

    await services.courses.send_answer(
        CoursePartQuestionAnswer(
            vk_id=event.peer_id,
            part_id=course_part.id,
            part_question_id=course_part.question_id,
            course_id=course.id,
            answer=answer,
        )
    )

    if course_part.is_last_part:
        await event.send_message(
            "Благодарю Вас за прохождение курса! Пожалуйста, оцените курс:",
            keyboard=make_rating_menu()
        )
    else:
        next_part_button = make_one_button_menu("Перейти к следующему уроку", {
            "cmd": "start_course",
            "course": course.model_dump()
        })
        courses_button = make_one_button_menu(
            "Выбор курса",
            {
                "cmd": "courses"
            }
        )

        await event.send_message(
            message=course_part.correct_text if answer == correct_answer_id else course_part.incorrect_text,
            keyboard=merge_inline_menus(
                merge_inline_menus(
                    next_part_button,
                    TO_MAIN_MENU_BUTTON
                ),
                courses_button
            ).get_json()
        )
