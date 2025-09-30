from vkbottle import BaseStateGroup


class Registration(BaseStateGroup):
    REGISTRATION_START = "registration_start"
    REGISTRATION_AGREEMENT = "registration_agreement"
    REGISTRATION_NAME = "registration_name"
    REGISTRATION_NAME_CONFIRMATION = "registration_name_confirmation"
    REGISTRATION_IS_MUSEUM_WORKER = "registration_is_museum_worker"
    HOW_LONG_MUSEUM_WORKER = "registration_how_much_years"
    REGISTRATION_OCCUPATION = "registration_occupation"
    REGISTRATION_SUBMIT = "submit-registration"
