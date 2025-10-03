from vkbottle import Keyboard
from vkbottle_schemas.keyboard import KeyboardButtonSchema


def make_yes_no_menu(swapped_icons: bool = False, for_state: str | None = None):
    yes_label = "Да"
    no_label = "Нет"

    return Keyboard(one_time=False, inline=True).schema([
        [KeyboardButtonSchema(
            label=yes_label,
            payload={"cmd": "yes", "state": for_state},
            type="callback"
        ).positive().get_json()],
        [KeyboardButtonSchema(
            label=no_label,
            payload={"cmd": "no", "state": for_state},
            type="callback"
        ).negative().get_json()],
    ]).get_json()


def make_confirmation_menu(for_state: str):
    return Keyboard(one_time=False, inline=True).schema([
        [KeyboardButtonSchema(
            label="Подтвердить",
            payload={"cmd": "confirm", "state": for_state},
            type="callback"
        ).positive().get_json()],
        [KeyboardButtonSchema(
            label="Отмена",
            payload={"cmd": "not_confirm", "state": for_state},
            type="callback"
        ).negative().get_json()],
    ]).get_json()


def make_skip_menu(for_state: str | None = None):
    return Keyboard(one_time=False, inline=True).schema([
        [KeyboardButtonSchema(
            label="Пропустить",
            payload={"cmd": "skip", "state": for_state},
            type="callback"
        ).secondary().get_json()],
    ]).get_json()


def make_cancel_menu(for_state: str | None = None):
    return Keyboard(one_time=False, inline=True).schema([
        [KeyboardButtonSchema(
            label="Отмена",
            payload={"cmd": "cancel", "state": for_state},
            type="callback"
        ).negative().get_json()],
    ]).get_json()


def make_user_agreement_menu(for_state: str | None = None):
    return Keyboard(one_time=False, inline=True).schema([
        [KeyboardButtonSchema(
            label="Да",
            payload={"cmd": "agree", "state": for_state},
            type="callback"
        ).positive().get_json()],
        [KeyboardButtonSchema(
            label="Нет",
            payload={"cmd": "not_agree", "state": for_state},
            type="callback"
        ).negative().get_json()],
    ]).get_json()


def make_rating_menu(course_id: int, for_state: str | None = None):
    keyboard = Keyboard(inline=True)
    schema = []

    for i in range(5, 0, -1):
        schema.append([
            KeyboardButtonSchema(
                label=str(i),
                payload={"cmd": "rate_course", "rate": i, "course_id": course_id},
                type="callback"
            ).get_json()
        ])

    return keyboard.schema(schema).get_json()
