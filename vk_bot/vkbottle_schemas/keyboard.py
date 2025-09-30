from typing import Any, Literal
from vkbottle.tools.keyboard.color import KeyboardButtonColor
from pydantic import BaseModel, Field


class KeyboardButtonSchema(BaseModel):
    label: str
    payload: str | dict[str, Any] | None = Field(None, alias="payload")
    type: Literal["text", "open_link", "callback", "location", "vkpay", "open_app"] = "text"
    color: str | None = None

    def primary(self) -> "KeyboardButtonSchema":
        self.color = KeyboardButtonColor.PRIMARY.value
        return self

    def secondary(self) -> "KeyboardButtonSchema":
        self.color = KeyboardButtonColor.SECONDARY.value
        return self

    def positive(self) -> "KeyboardButtonSchema":
        self.color = KeyboardButtonColor.POSITIVE.value
        return self

    def negative(self) -> "KeyboardButtonSchema":
        self.color = KeyboardButtonColor.NEGATIVE.value
        return self

    def text(self) -> "KeyboardButtonSchema":
        self.type = "text"
        return self

    def open_link(self) -> "KeyboardButtonSchema":
        self.type = "open_link"
        return self

    def callback(self) -> "KeyboardButtonSchema":
        self.type = "callback"
        return self

    def location(self) -> "KeyboardButtonSchema":
        self.type = "location"
        return self

    def vkpay(self) -> "KeyboardButtonSchema":
        self.type = "vkpay"
        return self

    def open_app(self) -> "KeyboardButtonSchema":
        self.type = "open_app"
        return self

    def get_json(self) -> dict[str, Any]:
        return self.model_dump()
