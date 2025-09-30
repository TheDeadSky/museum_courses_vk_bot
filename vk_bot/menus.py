from vkbottle import Keyboard

from vkbottle_schemas.keyboard import KeyboardButtonSchema

MAIN_MENU = Keyboard(one_time=False, inline=True).schema([
    [KeyboardButtonSchema(
        label="Пройти обучение",
        payload={"cmd": "courses"},
        type="callback"
    ).primary().get_json()],
    # [KeyboardButtonSchema(
    #     label="Поделиться опытом",
    #     payload={"cmd": "share_experience"},
    #     type="callback"
    # ).primary().get_json()],
    # [KeyboardButtonSchema(
    #     label="Обратная связь",
    #     payload={"cmd": "feedback"},
    #     type="callback"
    # ).primary().get_json()],
    [KeyboardButtonSchema(
        label="О проекте",
        payload={"cmd": "about_project"},
        type="callback"
    ).secondary().get_json()],
])

TO_MAIN_MENU_BUTTON = Keyboard(one_time=False, inline=True).schema([
    [KeyboardButtonSchema(
        label="В главное меню",
        payload={"cmd": "main_menu"},
        type="callback"
    ).secondary().get_json()],
])

GET_SUPPORT_MENU = Keyboard(one_time=False, inline=True).schema([
    [KeyboardButtonSchema(
        label="Пройти курс самоподдержки",
        payload={"cmd": "self_support_course"},
        type="callback"
    ).primary().get_json()],
    [KeyboardButtonSchema(
        label="Узнать истории коллег",
        payload={"cmd": "colleagues_stories"},
        type="callback"
    ).primary().get_json()],
])

ONE_MORE_STORY_BUTTON = Keyboard(one_time=False, inline=True).schema([
    [KeyboardButtonSchema(
        label="Узнать еще одну историю",
        payload={"cmd": "one_more_story"},
        type="callback"
    ).primary().get_json()],
])

NEXT_PART_BUTTON = Keyboard(one_time=False, inline=True).schema([
    [KeyboardButtonSchema(
        label="Смотреть следующую лекцию",
        payload={"cmd": "self_support_next_part"},
        type="callback"
    ).primary().get_json()],
])

HOW_MUCH_YEARS_MENU = Keyboard(one_time=False, inline=True).schema([
    [KeyboardButtonSchema(
        label="Менее 2-х лет",
        payload={
            "cmd": "how_much_years",
            "data": "lt2"
        },
        type="callback"
    ).get_json()],
    [KeyboardButtonSchema(
        label="От 2 до 5 лет",
        payload={
            "cmd": "how_much_years",
            "data": "f2t5"
        },
        type="callback"
    ).get_json()],
    [KeyboardButtonSchema(
        label="От 5 до 10 лет",
        payload={
            "cmd": "how_much_years",
            "data": "f5t10"
        },
        type="callback"
    ).get_json()],
    [KeyboardButtonSchema(
        label="Более 10 лет",
        payload={
            "cmd": "how_much_years",
            "data": "mt10"
        },
        type="callback"
    ).get_json()]
]).get_json()
