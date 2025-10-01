from vkbottle.bot import BotLabeler, Message

from actions.general import make_user_agreement_menu
from actions.main_menu import default_main_menu
from services.api_service import get_text_from_db
from menus import MAIN_MENU
from states.registration import Registration
from settings import state_dispenser, photo_message_uploader, services
from utils import fetch_binary_data

commands_labeler = BotLabeler()


@commands_labeler.message(text=["Начать", "начать", "Старт", "старт"])
async def start_handler(message: Message):
    vk_id = str(message.from_id)
    user_data = await message.get_user()

    registration_check = await services.registration.check(vk_id)

    if registration_check.is_registered:
        main_menu_text = await get_text_from_db("main_menu_text")
        await default_main_menu(
            message,
            main_menu_text
        )
        return

    await state_dispenser.set(
        message.peer_id,
        Registration.REGISTRATION_AGREEMENT,
        {
            "firstname": user_data.first_name,
            "lastname": user_data.last_name
        }
    )

    greetings = await get_text_from_db("start_greetings")

    await message.answer(
        greetings,
        keyboard=make_user_agreement_menu(Registration.REGISTRATION_AGREEMENT.value)
    )


@commands_labeler.message(command="/dev_menu")
async def menu_handler(message: Message):
    await message.answer("Главное меню:", keyboard=MAIN_MENU.get_json())


@commands_labeler.message(command="test_vid")
async def test_vid_handler(message: Message):
    await message.answer("🎥 Видео:")
    await message.answer(attachment="clip-229734251_456239028")


@commands_labeler.message(command="test_ph")
async def test_ph_handler(message: Message):
    photo_data = await fetch_binary_data("https://ideasformuseums.com/botimages/img_lec1.jpg")

    photo = await photo_message_uploader.upload(
        photo_data,
        message.peer_id
    )

    await message.answer("Фото:", attachment=photo)
