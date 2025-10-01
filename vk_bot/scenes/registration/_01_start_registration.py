from vkbottle.bot import BotLabeler, MessageEvent
from vkbottle_types.objects import UsersUserFull

from actions.general import make_user_agreement_menu
from customs.events import callback_handler
from states.registration import Registration
from services.api_service import get_text_from_db
from utils import update_state


def init(labeler: BotLabeler):
    @callback_handler(labeler, cmd="registration", state=Registration.REGISTRATION_START.value)
    async def start_registration(event: MessageEvent):
        await event.send_empty_answer()
        raw_user = (await event.ctx_api.request("users.get", {"user_ids": event.peer_id}))[
            "response"
        ][0]

        user_data = UsersUserFull(**raw_user)

        await update_state(
            event.peer_id,
            Registration.REGISTRATION_AGREEMENT,
            {
                "firstname": user_data.first_name,
                "lastname": user_data.last_name
            }
        )

        user_agreement_message = await get_text_from_db("user_agreement_message")
        agreement_menu = make_user_agreement_menu(
            for_state=Registration.REGISTRATION_AGREEMENT.value
        )
        await event.send_message(
            user_agreement_message,
            keyboard=agreement_menu
        )
