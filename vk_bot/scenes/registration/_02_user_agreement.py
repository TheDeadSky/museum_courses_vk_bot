from vkbottle.bot import BotLabeler, MessageEvent

from actions.registration import make_registration_button
from customs.events import callback_handler
from states.registration import Registration
from services.api_service import get_text_from_db
from settings import state_dispenser
from actions.general import make_yes_no_menu

def init(labeler: BotLabeler):
    @callback_handler(labeler, cmd="not_agree", state=Registration.REGISTRATION_AGREEMENT.value)
    async def user_not_agree(event: MessageEvent):
        await event.send_empty_answer()
        user_not_agree_message = await get_text_from_db("user_not_agree_message")
        await event.send_message(
            user_not_agree_message,
            keyboard=make_registration_button(
                "Старт"
            )
        )

    @callback_handler(labeler, cmd="agree", state=Registration.REGISTRATION_AGREEMENT.value)
    async def confirm(event: MessageEvent):
        await event.send_empty_answer()
        await event.send_message("Благодарю за доверие! Нам с командой важно знать, кто интересуется проектом «Лаборатория музейного интеллекта», поэтому зададим Вам пару вопросов.")
        await state_dispenser.set(
            event.peer_id,
            Registration.REGISTRATION_IS_MUSEUM_WORKER
        )
        is_museum_worker_question = await get_text_from_db("is_museum_worker_question")
        await event.send_message(
            is_museum_worker_question,
            keyboard=make_yes_no_menu(for_state=Registration.REGISTRATION_IS_MUSEUM_WORKER.value)
        )
