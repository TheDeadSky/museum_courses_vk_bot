from vkbottle.bot import BotLabeler, Message, MessageEvent

from customs.events import callback_handler
from menus import TO_MAIN_MENU_BUTTON
from models.courses import CourseFeedback
from services import get_text_from_db
from settings import services
from states.courses import Courses
from states.general_states import GeneralStates
from utils import update_state, get_state_payload

course_feedback_labeler = BotLabeler()


@callback_handler(course_feedback_labeler, cmd="rate_course")
async def rate_course(event: MessageEvent):
    await event.send_empty_answer()
    course_id = event.payload["course_id"]
    rate = event.payload["rate"]

    await update_state(
        event.peer_id,
        Courses.RATE_DESCRIPTION,
        {
            "course_id": course_id,
            "rate": rate,
        }
    )

    ask_rate_description = await get_text_from_db("ask_rate_description")
    await event.send_message(
        ask_rate_description
    )


@course_feedback_labeler.message(state=Courses.RATE_DESCRIPTION)
async def rate_description_handler(message: Message):
    rate_description = message.text

    await update_state(
        message.peer_id,
        Courses.PUBLIC_FEEDBACK,
        {
            "rate_description": rate_description
        }
    )

    ask_course_feedback = await get_text_from_db("ask_course_feedback")
    await message.answer(ask_course_feedback)


@course_feedback_labeler.message(state=Courses.PUBLIC_FEEDBACK)
async def public_feedback_handler(message: Message):
    public_feedback = message.text

    await update_state(
        message.peer_id,
        Courses.PUBLIC_FEEDBACK,
        {
            "vk_id": message.peer_id,
            "public_feedback": public_feedback
        }
    )

    payload = await get_state_payload(message.peer_id)
    course_feedback = CourseFeedback(**payload)
    await services.courses.send_feedback(course_feedback)

    await update_state(
        message.peer_id,
        GeneralStates.MAIN_MENU
    )
    course_final_thanks = await get_text_from_db("course_final_thanks")
    await message.answer(course_final_thanks, keyboard=TO_MAIN_MENU_BUTTON)
