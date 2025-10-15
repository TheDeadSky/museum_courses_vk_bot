import asyncio

from vkbottle import Keyboard, Callback
from vkbottle.bot import BotLabeler, MessageEvent

from customs.events import callback_handler
from menus import TO_MAIN_MENU_BUTTON
from settings import services, video_uploader
from utils import make_one_button_menu

course_labeler = BotLabeler()


@callback_handler(course_labeler, cmd="start_course")
async def start_course(event: MessageEvent):
    await event.send_empty_answer()
    course = await services.courses.get_course(event.payload["course_id"])
    course_part = await services.courses.get_next_part(event.peer_id, course.id)

    if course_part is None:
        await event.send_message(
            "Не удалось загрузить следующий урок.\n\nПопробуйте позже.",
            keyboard=TO_MAIN_MENU_BUTTON
        )
        return

    await event.send_message("🎥 Видео:")
    await event.send_message(
        attachment=course_part.video_url,
        keyboard=make_one_button_menu(
            "Открыть текст урока",
            {
                "cmd":"show_course_text",
                "course_id": event.payload["course_id"]
            }
        ).get_json()
    )


@callback_handler(course_labeler, cmd="show_course_text")
async def show_course_text(event: MessageEvent):
    await event.send_empty_answer()
    course = await services.courses.get_course(event.payload["course_id"])
    course_part = await services.courses.get_next_part(event.peer_id, course.id)

    part_title = course_part.title
    part_description = course_part.description
    await event.send_message(
        f"{part_title}\n\n{part_description}"
    )
    await event.send_message(
        "⏩",
        keyboard=make_one_button_menu(
            "Пройти тест",
            {
                "cmd": "goto_test",
                "course_id": event.payload["course_id"]
            }
        ).get_json()
    )


@callback_handler(course_labeler, cmd="goto_test")
async def goto_test(event: MessageEvent):
    await event.send_empty_answer()
    course = await services.courses.get_course(event.payload["course_id"])
    course_part = await services.courses.get_next_part(event.peer_id, course.id)

    answers = Keyboard(inline=True).add(
        Callback(
            label=course_part.answer_1,
            payload={
                "cmd": "answer_question",
                "correct_answer": course_part.correct_answer,
                "answer": 1,
                "part_id": course_part.id,
                "course_id": course.id
            }
        )
    ).row().add(
        Callback(
            label=course_part.answer_2,
            payload={
                "cmd": "answer_question",
                "correct_answer": course_part.correct_answer,
                "answer": 2,
                "part_id": course_part.id,
                "course_id": course.id
            }
        )
    ).row().add(
        Callback(
            label=course_part.answer_3,
            payload={
                "cmd": "answer_question",
                "correct_answer": course_part.correct_answer,
                "answer": 3,
                "part_id": course_part.id,
                "course_id": course.id
            }
        )
    ).row().add(
        Callback(
            label=course_part.answer_4,
            payload={
                "cmd": "answer_question",
                "correct_answer": course_part.correct_answer,
                "answer": 4,
                "part_id": course_part.id,
                "course_id": course.id
            }
        )
    )

    await event.send_message(
        f"📝 Тест к уроку\n\n{course_part.question}",
        keyboard=answers.get_json()
    )
