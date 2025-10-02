import aiohttp
from typing import Any, Literal

from vkbottle import Keyboard, BaseStateGroup

from settings import state_dispenser
from vkbottle_schemas.keyboard import KeyboardButtonSchema


def merge_inline_menus(first_menu: Keyboard, second_menu: Keyboard) -> Keyboard:
    keyboard = Keyboard(one_time=False, inline=True)

    keyboard.buttons = [
        *first_menu.buttons,
        *second_menu.buttons
    ]

    return keyboard


def make_one_button_menu(
    text: str,
    payload: dict[str, Any],
    _type: Literal["text", "open_link", "callback", "location", "vkpay", "open_app"] = "callback"
) -> Keyboard:
    return Keyboard(one_time=False, inline=True).schema([
        [KeyboardButtonSchema(label=text, payload=payload, type=_type).primary().get_json()],
    ])


async def fetch_binary_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Ошибка загрузки: HTTP {response.status}")
            return await response.read()


async def get_state_payload(peer_id: int):
    state_peer = await state_dispenser.get(peer_id)

    if state_peer is None:
        return {}

    return state_peer.payload


async def update_state(peer_id: int, state: None | BaseStateGroup, payload: None | dict[str, Any] = None):
    state_payload = await get_state_payload(peer_id)
    if payload is not None:
        state_payload.update(payload)

    await state_dispenser.set(
        peer_id,
        state,
        **state_payload
    )
