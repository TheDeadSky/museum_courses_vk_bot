from vkbottle.bot import BotLabeler, MessageEvent

from actions.registration import submit_registration
from constants import YEARS_MAP
from customs.events import callback_handler
from states.registration import Registration
from utils import update_state, get_state_payload


def init(labeler: BotLabeler):
    @callback_handler(labeler, cmd="how_much_years")
    async def how_long_museum_worker_handler(event: MessageEvent):
        await event.send_empty_answer()
        how_long_museum_worker = YEARS_MAP[event.payload["data"]]
        await update_state(
            event.peer_id,
            Registration.REGISTRATION_SUBMIT,
            payload={
                "how_long_museum_worker": how_long_museum_worker
            }
        )

        registration_data = await get_state_payload(event.peer_id)

        await submit_registration(event, registration_data)