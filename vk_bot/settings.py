import logging
import os
from vkbottle import (
    API,
    BuiltinStateDispenser,
    VideoUploader,
    VoiceMessageUploader,
    PhotoMessageUploader
)
from vkbottle.bot import BotLabeler
from vkbottle.callback import BotCallback

from services.api_service import JsonApiService
from services.hub import ServicesHub

APP_NAME = "Museum VK Bot"
APP_VERSION = "1.0.0"
TOKEN = os.getenv("VK_BOT_TOKEN")
GROUP_ID = os.getenv("VK_GROUP_ID", None)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/vk-bot/callback")
WEBAPP_HOST = os.getenv("WEBAPP_HOST", "0.0.0.0")
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT", "9001"))
VK_SECRET_KEY = os.getenv("VK_SECRET_KEY", "")
VK_CONFIRMATION_CODE = os.getenv("VK_CONFIRMATION_CODE", "")
API_BASE_URL = os.getenv("API_BASE_URL", "http://museum_api:8000")


if TOKEN is None:
    raise RuntimeError("VK_BOT_TOKEN not found")

museum_api = JsonApiService(API_BASE_URL)
services = ServicesHub(api_service=museum_api)

api = API(TOKEN)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()
voice_uploader = VoiceMessageUploader(
    api=api
)
video_uploader = VideoUploader(
    api=api
)
photo_message_uploader = PhotoMessageUploader(
    api=api
)
callback = BotCallback(
    url=WEBHOOK_URL,
    title="My Webhook",
    secret_key=VK_SECRET_KEY,
    api=api,
    group_id=GROUP_ID
)
