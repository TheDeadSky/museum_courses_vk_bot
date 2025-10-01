from abc import ABC

from services.api_service import JsonApiService
from services.memory_cache import MemoryCacheService


class AbstractEntityService(ABC):
    module: str

    def __init__(self, api_service: JsonApiService, cache_service: MemoryCacheService):
        self._api_service = api_service
        self._cache_service = cache_service
