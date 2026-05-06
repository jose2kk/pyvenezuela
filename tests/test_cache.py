"""InMemoryCache Tests."""

import time

from pyvenezuela.cache import InMemoryCache


def test_set_and_get__stores_and_retrieves_value() -> None:
    cache = InMemoryCache()
    cache.set("key1", "value1", ttl_in_seconds=60)

    result = cache.get("key1")
    assert result is not None
    assert result.value == "value1"


def test_get__nonexistent_key_returns_none() -> None:
    cache = InMemoryCache()
    assert cache.get("nonexistent") is None


def test_set__ttl_is_set_correctly() -> None:
    cache = InMemoryCache()
    before = time.time()
    cache.set("key1", "value1", ttl_in_seconds=120)
    after = time.time()

    result = cache.get("key1")
    assert result is not None
    assert before + 120 <= result.expires_at <= after + 120


def test_set_and_get__multiple_keys_work_independently() -> None:
    cache = InMemoryCache()
    cache.set("key1", "value1", ttl_in_seconds=60)
    cache.set("key2", "value2", ttl_in_seconds=120)

    result1 = cache.get("key1")
    result2 = cache.get("key2")

    assert result1 is not None
    assert result1.value == "value1"

    assert result2 is not None
    assert result2.value == "value2"

    # TTLs should differ
    assert result2.expires_at > result1.expires_at
