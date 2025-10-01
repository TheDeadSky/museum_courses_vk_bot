from pydantic import BaseModel

from schemas import BaseResponse


class RegistrationData(BaseModel):
    vk_id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    is_museum_worker: bool = False
    museum_name: str | None = None
    occupation: str | None = None
    how_long_museum_worker: str | None = None


class RegistrationResponse(BaseResponse):
    pass


class RegistrationCheckResponse(BaseModel):
    is_registered: bool = False
    vk_id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
