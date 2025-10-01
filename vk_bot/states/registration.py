from vkbottle import BaseStateGroup


class Registration(BaseStateGroup):
    REGISTRATION_START = "registration_start"
    REGISTRATION_AGREEMENT = "registration_agreement"
    REGISTRATION_IS_MUSEUM_WORKER = "registration_is_museum_worker"
    MUSEUM_NAME = "registration_museum_name"
    HOW_LONG_MUSEUM_WORKER = "registration_how_much_years"
    REGISTRATION_OCCUPATION = "registration_occupation"
    REGISTRATION_SUBMIT = "submit-registration"
