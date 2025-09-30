import sentry_sdk
from vkbottle import Bot

from handlers.commands.main_commands import commands_labeler
from scenes.registration import registration_labeler
from scenes.main_menu import main_menu_labeler
from scenes.courses import courses_labeler
from settings import state_dispenser, labeler, api, callback

sentry_sdk.init("https://9485268e8cff4009a5e148f812472fad@errors.asarta.ru/12")

bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
    callback=callback
)

bot.labeler.load(commands_labeler)
bot.labeler.load(registration_labeler)
bot.labeler.load(main_menu_labeler)
bot.labeler.load(courses_labeler)
# bot.labeler.load(get_support_labeler)
# bot.labeler.load(share_experience_labeler)
# bot.labeler.load(feedback_labeler)
