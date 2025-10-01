import time
from typing import Any

DEFAULT_LIFETIME = 3600


class MemoryCacheService:
    def __init__(self):
        self._cache: dict[str, dict[str, Any]] = {}

    def get(self, key: str | int) -> Any | None:
        if key in self._cache:
            data = self._cache.get(key)
            lifetime = time.time() - data["timestamp"]
            if lifetime > data["max_lifetime"]:
                return None
            return data
        return None

    def update(self, key: str | int, data: Any, max_lifetime=DEFAULT_LIFETIME) -> None:
        self._cache[key] = {
            "value": data,
            "timestamp": time.time(),
            "max_lifetime": max_lifetime
        }

    def clear(self) -> None:
        self._cache = {}

    def remove(self, key: str | int) -> None:
        del self._cache[key]
