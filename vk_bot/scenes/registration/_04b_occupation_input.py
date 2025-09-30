from vkbottle.bot import Message, BotLabeler

from states.registration import Registration
from actions.registration import submit_registration
from utils import get_state_payload, update_state


def init(labeler: BotLabeler):
    @labeler.message(state=Registration.REGISTRATION_OCCUPATION)
    async def occupation_input_handler(message: Message):
        await update_state(
            message.peer_id,
            Registration.REGISTRATION_OCCUPATION,
            {
                "occupation": message.text
            }
        )
        await submit_registration(message, await get_state_payload(message.peer_id))
