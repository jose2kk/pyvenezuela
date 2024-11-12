"""Decorators."""

import functools
import time
from typing import Any, Callable, Optional

from pyvenezuela.cache import Cache
from pyvenezuela.schemas.cache import CacheValueModel


def cached(
    cache: Cache,
    cached_key: str,
    ttl_in_seconds: int,
    use_expired: bool = False,
) -> Callable:
    def _handle_function_call(f: Callable, *args, **kwargs) -> Optional[CacheValueModel]:
        """In case there is an error with the function call, None is returned."""
        try:
            return f(*args, **kwargs)
        except Exception:
            return None

    def decorator(f: Callable):
        @functools.wraps(f)
        def inner(*args, **kwargs) -> Any:
            cached_value_model = cache.get(cached_key)
            if cached_value_model and cached_value_model.expires_at > time.time():
                return cached_value_model.value
            elif cached_value_model and cached_value_model.expires_at <= time.time():
                result = _handle_function_call(f, *args, **kwargs)
                if result:
                    cache.set(cached_key, result, ttl_in_seconds=ttl_in_seconds)
                    return result
                elif use_expired:
                    return cached_value_model.value
            else:  # not cached_value_model
                result = _handle_function_call(f, *args, **kwargs)
                if result:
                    cache.set(cached_key, result, ttl_in_seconds=ttl_in_seconds)
                    return result
                return None
        return inner
    return decorator
