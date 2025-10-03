import asyncio

from vkbottle.bot import BotLabeler, MessageEvent

from actions.general import make_rating_menu
from customs.events import callback_handler
from menus import TO_MAIN_MENU_BUTTON
from models.courses import CoursePartQuestionAnswer
from services import get_text_from_db
from settings import services
from utils import make_one_button_menu, merge_inline_menus

course_question_labeler = BotLabeler()


@callback_handler(course_question_labeler, cmd="answer_question")
async def start_course(event: MessageEvent):
    await event.send_empty_answer()

    event_payload = event.payload
    course = await services.courses.get_course(event_payload["course_id"])
    course_part = await services.courses.get_part(course.id, event_payload["part_id"])
    answer = event_payload["answer"]
    correct_answer = event_payload["correct_answer"]

    await services.courses.send_answer(
        CoursePartQuestionAnswer(
            vk_id=event.peer_id,
            part_id=course_part.id,
            part_question_id=course_part.question_id,
            course_id=course.id,
            answer=str(answer),
        )
    )

    print(course_part.model_dump())

    if course_part.last_part:
        await event.send_message(
            message=course_part.correct_message if answer == correct_answer else course_part.incorrect_message,
        )
        await asyncio.sleep(2)
        ask_rate = await get_text_from_db("ask_rate")
        await event.send_message(
            ask_rate,
            keyboard=make_rating_menu(course.id)
        )
        return

    next_part_button = make_one_button_menu("Перейти к следующему уроку", {
        "cmd": "start_course",
        "course_id": course.id
    })
    courses_button = make_one_button_menu(
        "Выбор курса",
        {
            "cmd": "courses"
        }
    )

    await event.send_message(
        message=course_part.correct_message if answer == correct_answer else course_part.incorrect_message,
        keyboard=merge_inline_menus(
            merge_inline_menus(
                next_part_button,
                TO_MAIN_MENU_BUTTON
            ),
            courses_button
        ).get_json()
    )
