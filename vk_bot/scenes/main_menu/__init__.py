from vkbottle.bot import Message, BotLabeler, MessageEvent

from actions.main_menu import default_main_menu
from customs.events import callback_handler
from menus import TO_MAIN_MENU_BUTTON
from services.api_service import get_text_from_db


main_menu_labeler = BotLabeler()


@main_menu_labeler.message(text="меню")
@main_menu_labeler.message(command="/menu")
async def on_main_menu_handler(message: Message):
    main_menu_text = await get_text_from_db("main_menu_text")
    await default_main_menu(message, main_menu_text=main_menu_text)


@callback_handler(main_menu_labeler, cmd="main_menu")
async def on_main_menu_callback_handler(event: MessageEvent):
    await event.send_empty_answer()
    main_menu_text = await get_text_from_db("main_menu_text")
    await default_main_menu(event, main_menu_text=main_menu_text)


@callback_handler(main_menu_labeler, cmd="about_project")
async def about_project(event: MessageEvent):
    await event.send_empty_answer()
    about_project_text = await get_text_from_db("about_project_text")
    await event.send_message(about_project_text, keyboard=TO_MAIN_MENU_BUTTON.get_json())

__all__ = ["main_menu_labeler"]
