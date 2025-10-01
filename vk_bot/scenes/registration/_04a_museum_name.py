from vkbottle.bot import Message, BotLabeler

from menus import HOW_MUCH_YEARS_MENU
from services import get_text_from_db
from states.registration import Registration
from utils import update_state


def init(labeler: BotLabeler):
    @labeler.message(state=Registration.MUSEUM_NAME)
    async def museum_input_handler(message: Message):
        await update_state(
            message.peer_id,
            Registration.HOW_LONG_MUSEUM_WORKER,
            {
                "museum_name": message.text
            }
        )

        await message.answer("Спасибо!")

        how_long_museum_worker = await get_text_from_db("how_long_museum_worker")
        await message.answer(
            how_long_museum_worker,
            keyboard=HOW_MUCH_YEARS_MENU
        )
