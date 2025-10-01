from services.api_service import JsonApiService
from services.entities.courses import CoursesService
from services.entities.registration import RegistrationService
from services.memory_cache import MemoryCacheService


class ServicesHub:
    def __init__(
        self,
        base_url: None | str = None,
        api_service: None | JsonApiService = None
    ):
        if api_service:
            self._api_service = api_service
        else:
            self._api_service = JsonApiService(base_url)

        self._cache_service = MemoryCacheService()
        self._registration_service = RegistrationService(self._api_service, self._cache_service)
        self._courses_service = CoursesService(self._api_service, self._cache_service)

    @property
    def api(self) -> JsonApiService:
        return self._api_service

    @property
    def cache(self) -> MemoryCacheService:
        return self._cache_service

    @property
    def registration(self) -> RegistrationService:
        return self._registration_service

    @property
    def courses(self) -> CoursesService:
        return self._courses_service
