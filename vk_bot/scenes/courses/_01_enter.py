from vkbottle.bot import BotLabeler, MessageEvent

from actions.courses import make_courses_menu
from customs.events import callback_handler
from menus import TO_MAIN_MENU_BUTTON
from models.courses import CourseInfo
from services.api_service import get_text_from_db
from settings import services
from utils import merge_inline_menus, make_one_button_menu

courses_enter_labeler = BotLabeler()


@callback_handler(courses_enter_labeler, cmd="courses")
async def on_enter_courses(event: MessageEvent):
    await event.send_empty_answer()
    about_courses_message = await get_text_from_db("about_courses_message")
    courses = await services.courses.list(event.peer_id)

    await event.send_message(
        about_courses_message,
        keyboard = merge_inline_menus(
            make_courses_menu(courses),
            TO_MAIN_MENU_BUTTON
        ).get_json()
    )

@callback_handler(courses_enter_labeler, cmd="show_course")
async def show_course(event: MessageEvent):
    await event.send_empty_answer()
    course = CourseInfo(**event.payload["course"])

    start_course_button = make_one_button_menu(
        text="Продолжить курс" if course.is_started else "Начать курс",
        payload={
            "cmd": "start_course",
            "course": course.model_dump(),
        }
    )

    await event.send_message(
        course.description,
        keyboard=merge_inline_menus(
            start_course_button,
            TO_MAIN_MENU_BUTTON
        ).get_json()
    )
