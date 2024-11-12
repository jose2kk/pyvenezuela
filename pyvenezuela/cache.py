"""Cache."""

import abc
import time
from typing import Any, Dict, Optional

from pyvenezuela.schemas.cache import CacheValueModel


class Cache:
    """Cache."""

    @abc.abstractmethod
    def get(self, key: str) -> Optional[CacheValueModel]:
        raise NotImplementedError("Child needs to implement `get` method.")

    @abc.abstractmethod
    def set(self, key: str, value: Any, ttl_in_seconds: int) -> None:
        raise NotImplementedError("Child needs to implement `set` method.")


class InMemoryCache(Cache):
    """In Memory Cache."""

    def __init__(self) -> None:
        self.cache: Dict[str, CacheValueModel] = {}

    def get(self, key: str) -> Optional[CacheValueModel]:
        return self.cache.get(key)

    def set(self, key: str, value: Any, ttl_in_seconds: int) -> None:
        self.cache[key] = CacheValueModel(
            value=value,
            expires_at=time.time() + ttl_in_seconds,
        )


inmemory_cache = InMemoryCache()
