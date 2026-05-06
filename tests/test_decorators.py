"""Decorators Tests."""

from unittest.mock import MagicMock, patch

from pyvenezuela.cache import InMemoryCache
from pyvenezuela.decorators import cached


def test_cached__first_call_executes_and_caches() -> None:
    cache = InMemoryCache()
    mock_fn = MagicMock(return_value="result")

    @cached(cache=cache, cached_key="test_key", ttl_in_seconds=60)
    def my_func():
        return mock_fn()

    result = my_func()

    assert result == "result"
    mock_fn.assert_called_once()
    assert cache.get("test_key") is not None
    assert cache.get("test_key").value == "result"


def test_cached__second_call_within_ttl_returns_cached() -> None:
    cache = InMemoryCache()
    mock_fn = MagicMock(return_value="result")

    @cached(cache=cache, cached_key="test_key", ttl_in_seconds=60)
    def my_func():
        return mock_fn()

    my_func()
    result = my_func()

    assert result == "result"
    mock_fn.assert_called_once()


def test_cached__call_after_ttl_expiry_re_executes() -> None:
    cache = InMemoryCache()
    call_count = 0

    @cached(cache=cache, cached_key="test_key", ttl_in_seconds=10)
    def my_func():
        nonlocal call_count
        call_count += 1
        return f"result_{call_count}"

    # First call
    with patch("pyvenezuela.decorators.time") as mock_time:
        mock_time.time.return_value = 1000.0
        # Also patch the cache's time so expires_at is set correctly
        with patch("pyvenezuela.cache.time") as mock_cache_time:
            mock_cache_time.time.return_value = 1000.0
            result1 = my_func()

    assert result1 == "result_1"
    assert call_count == 1

    # Second call after TTL expired
    with patch("pyvenezuela.decorators.time") as mock_time:
        mock_time.time.return_value = 1011.0
        with patch("pyvenezuela.cache.time") as mock_cache_time:
            mock_cache_time.time.return_value = 1011.0
            result2 = my_func()

    assert result2 == "result_2"
    assert call_count == 2


def test_cached__use_expired_true_returns_stale_on_failure() -> None:
    cache = InMemoryCache()
    call_count = 0

    @cached(cache=cache, cached_key="test_key", ttl_in_seconds=10, use_expired=True)
    def my_func():
        nonlocal call_count
        call_count += 1
        if call_count > 1:
            raise Exception("fail")
        return "original_result"

    # First call succeeds and caches
    with patch("pyvenezuela.decorators.time") as mock_time:
        mock_time.time.return_value = 1000.0
        with patch("pyvenezuela.cache.time") as mock_cache_time:
            mock_cache_time.time.return_value = 1000.0
            result1 = my_func()

    assert result1 == "original_result"

    # Second call after TTL, function fails, should return stale value
    with patch("pyvenezuela.decorators.time") as mock_time:
        mock_time.time.return_value = 1011.0
        result2 = my_func()

    assert result2 == "original_result"
    assert call_count == 2


def test_cached__use_expired_false_returns_none_on_failure() -> None:
    cache = InMemoryCache()
    call_count = 0

    @cached(cache=cache, cached_key="test_key", ttl_in_seconds=10, use_expired=False)
    def my_func():
        nonlocal call_count
        call_count += 1
        if call_count > 1:
            raise Exception("fail")
        return "original_result"

    # First call succeeds
    with patch("pyvenezuela.decorators.time") as mock_time:
        mock_time.time.return_value = 1000.0
        with patch("pyvenezuela.cache.time") as mock_cache_time:
            mock_cache_time.time.return_value = 1000.0
            result1 = my_func()

    assert result1 == "original_result"

    # Second call after TTL, function fails, use_expired=False so returns None
    with patch("pyvenezuela.decorators.time") as mock_time:
        mock_time.time.return_value = 1011.0
        result2 = my_func()

    assert result2 is None


def test_cached__exception_with_no_cached_value_returns_none() -> None:
    cache = InMemoryCache()

    @cached(cache=cache, cached_key="test_key", ttl_in_seconds=60)
    def my_func():
        raise Exception("fail")

    result = my_func()
    assert result is None
    assert cache.get("test_key") is None
