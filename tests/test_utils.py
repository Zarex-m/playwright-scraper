import pytest
from quote_scraper.utils import with_retries, RateLimiter


def test_retries_then_success():
    calls, sleeps = [], []
    def fn():
        calls.append(1)
        if len(calls) < 3:
            raise RuntimeError("boom")
        return "ok"
    assert with_retries(fn, retries=3, backoff=1, sleep=sleeps.append) == "ok"
    assert sleeps == [1, 2]


def test_retries_exhausted():
    with pytest.raises(RuntimeError):
        with_retries(lambda: (_ for _ in ()).throw(RuntimeError("x")), retries=2,
                     backoff=0, sleep=lambda s: None)


def test_rate_limiter_waits():
    t = [0.0]; slept = []
    def sleep(s): slept.append(s); t[0] += s
    rl = RateLimiter(1.0, clock=lambda: t[0], sleep=sleep)
    rl.wait(); t[0] += 0.3; rl.wait()
    assert slept == [pytest.approx(0.7)]
