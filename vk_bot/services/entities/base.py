from abc import ABC

from services.api_service import JsonApiService


class AbstractEntityService(ABC):
    module: str

    def __init__(self, api_service: JsonApiService):
        self.api_service = api_service
