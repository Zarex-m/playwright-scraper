"""Retry and rate-limit helpers (pure, unit-testable)."""
from __future__ import annotations

import logging
import time
from typing import Callable, TypeVar

T = TypeVar("T")
log = logging.getLogger(__name__)


def with_retries(fn: Callable[[], T], retries: int = 3, backoff: float = 2.0,
                 sleep: Callable[[float], None] = time.sleep,
                 exceptions: tuple[type[BaseException], ...] = (Exception,)) -> T:
    """Call fn, retrying up to `retries` times with exponential backoff."""
    attempt = 0
    while True:
        try:
            return fn()
        except exceptions as exc:  # noqa: PERF203
            if attempt >= retries:
                log.error("Giving up after %d attempts: %s", attempt + 1, exc)
                raise
            wait = backoff * (2 ** attempt)
            log.warning("Attempt %d failed (%s); retrying in %.1fs", attempt + 1, exc, wait)
            sleep(wait)
            attempt += 1


class RateLimiter:
    """Ensures at least `min_interval` seconds between calls to wait()."""

    def __init__(self, min_interval: float, clock: Callable[[], float] = time.monotonic,
                 sleep: Callable[[float], None] = time.sleep):
        self.min_interval = min_interval
        self._clock, self._sleep = clock, sleep
        self._last: float | None = None

    def wait(self) -> None:
        now = self._clock()
        if self._last is not None:
            remaining = self.min_interval - (now - self._last)
            if remaining > 0:
                self._sleep(remaining)
                now = self._clock()
        self._last = now
