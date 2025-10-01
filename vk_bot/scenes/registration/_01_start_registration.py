from vkbottle.bot import BotLabeler, MessageEvent

from actions.general import make_user_agreement_menu
from customs.events import callback_handler
from states.registration import Registration
from services.api_service import get_text_from_db


def init(labeler: BotLabeler):
    @callback_handler(labeler, cmd="registration", state=Registration.REGISTRATION_START.value)
    async def start_registration(event: MessageEvent):
        await event.send_empty_answer(keboard=None)
        user_agreement_message = await get_text_from_db("user_agreement_message")
        agreement_menu = make_user_agreement_menu(
            for_state=Registration.REGISTRATION_AGREEMENT.value
        )
        await event.send_message(
            user_agreement_message,
            keyboard=agreement_menu
        )
