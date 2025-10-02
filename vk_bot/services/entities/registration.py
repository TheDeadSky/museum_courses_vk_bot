import logging

from models import RegistrationData
from models.registration import RegistrationResponse, RegistrationCheckResponse
from services.entities.base import AbstractEntityService


class RegistrationService(AbstractEntityService):
    module = "registration"

    async def register(self, registration_data: RegistrationData) -> RegistrationResponse:
        try:
            response = await self._api_service.create(
                module=self.module,
                data=registration_data.model_dump()
            )

            return RegistrationResponse(**response)

        except Exception as e:
            print(f"RegistrationError for '{registration_data.vk_id}': {e}")
            return RegistrationResponse(success=False, message="Не удалось зарегистрироваться.")

    async def check(self, vk_id: str) -> RegistrationCheckResponse:
        try:
            resource = await self._api_service.read(
                module=self.module,
                data={
                    "vk_id": vk_id
                }
            )

            return RegistrationCheckResponse(**resource)
        except Exception as e:
            print(f"RegistrationError for '{vk_id}': {e}")
            return RegistrationCheckResponse(is_registered=False)
