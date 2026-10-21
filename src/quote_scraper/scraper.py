"""Core Playwright scraper with pagination, retries and rate limiting."""
from __future__ import annotations

import logging
from urllib.parse import urljoin

from playwright.sync_api import Page, sync_playwright, TimeoutError as PWTimeout

from .config import ScraperConfig
from .utils import RateLimiter, with_retries

log = logging.getLogger(__name__)

EXTRACT_JS = """
() => Array.from(document.querySelectorAll('div.quote')).map(q => ({
  text: (q.querySelector('.text')?.textContent || '').trim(),
  author: (q.querySelector('.author')?.textContent || '').trim(),
  tags: Array.from(q.querySelectorAll('.tag')).map(t => t.textContent.trim()),
}))
"""


def clean_text(text: str) -> str:
    return text.strip().strip("\u201c\u201d\"").strip()


def parse_page(page: Page, page_no: int, url: str) -> tuple[list[dict], str | None]:
    """Extract quotes from the current page and return (records, next_url)."""
    raw = page.evaluate(EXTRACT_JS)
    records = [{"text": clean_text(r["text"]), "author": r["author"], "tags": r["tags"],
                "page": page_no, "source_url": url} for r in raw]
    nxt = page.query_selector("li.next > a")
    next_url = urljoin(url, nxt.get_attribute("href")) if nxt else None
    return records, next_url


class QuoteScraper:
    def __init__(self, config: ScraperConfig):
        config.validate()
        self.config = config
        self.limiter = RateLimiter(config.delay)

    def _load(self, page: Page, url: str) -> None:
        def go():
            resp = page.goto(url, timeout=self.config.timeout_ms, wait_until="domcontentloaded")
            if resp is not None and resp.status >= 400:
                raise RuntimeError(f"HTTP {resp.status} for {url}")
            # JS pages render quotes client-side, so wait for them explicitly.
            page.wait_for_selector("div.quote", timeout=self.config.timeout_ms)
        with_retries(go, retries=self.config.retries, backoff=self.config.backoff,
                     exceptions=(PWTimeout, RuntimeError))

    def run(self) -> list[dict]:
        cfg = self.config
        results: list[dict] = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=cfg.headless)
            try:
                page = browser.new_context(user_agent=cfg.user_agent).new_page()
                url, page_no = cfg.start_url, 1
                while url:
                    if cfg.max_pages and page_no > cfg.max_pages:
                        break
                    self.limiter.wait()
                    log.info("Fetching page %d: %s", page_no, url)
                    self._load(page, url)
                    records, url = parse_page(page, page_no, page.url)
                    log.info("  -> %d quotes", len(records))
                    results.extend(records)
                    page_no += 1
            finally:
                browser.close()
        log.info("Done: %d quotes from %d pages", len(results), page_no - 1)
        return results
