from vkbottle.bot import BotLabeler

from . import (
    _01_start_registration,
    _02_user_agreement,
    _03_is_museum_worker,
    _04a_museum_name,
    _04b_occupation_input,
    _05_how_much_years
)

registration_labeler = BotLabeler()


_01_start_registration.init(registration_labeler)
_02_user_agreement.init(registration_labeler)
_03_is_museum_worker.init(registration_labeler)
_04a_museum_name.init(registration_labeler)
_04b_occupation_input.init(registration_labeler)
_05_how_much_years.init(registration_labeler)

__all__ = ["registration_labeler"]
