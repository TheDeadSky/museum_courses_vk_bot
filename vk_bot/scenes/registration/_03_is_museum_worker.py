from vkbottle.bot import BotLabeler, MessageEvent

from customs.events import callback_handler
from menus import HOW_MUCH_YEARS_MENU
from states.registration import Registration
from services.api_service import get_text_from_db
from utils import update_state


def init(labeler: BotLabeler):
    @callback_handler(labeler, cmd="yes", state=Registration.REGISTRATION_IS_MUSEUM_WORKER.value)
    async def yes(event: MessageEvent):
        await event.send_empty_answer()
        await update_state(
            event.peer_id,
            Registration.HOW_LONG_MUSEUM_WORKER,
            payload={
                "is_museum_worker": True
            }
        )
        how_long_museum_worker_question = await get_text_from_db("how_long_museum_worker")
        await event.send_message(
            how_long_museum_worker_question,
            keyboard=HOW_MUCH_YEARS_MENU
        )

    @callback_handler(labeler, cmd="no", state=Registration.REGISTRATION_IS_MUSEUM_WORKER.value)
    async def no(event: MessageEvent):
        await event.send_empty_answer()
        await update_state(
            event.peer_id,
            Registration.HOW_LONG_MUSEUM_WORKER,
            payload={
                "is_museum_worker": False
            }
        )
        occupation_question = await get_text_from_db("occupation_question")
        await event.send_message(occupation_question)
