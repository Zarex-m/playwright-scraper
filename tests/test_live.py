import os
import pytest
from quote_scraper.config import ScraperConfig
from quote_scraper.scraper import QuoteScraper

pytestmark = [pytest.mark.network,
              pytest.mark.skipif(os.getenv("SKIP_NETWORK") == "1", reason="SKIP_NETWORK=1")]


@pytest.mark.parametrize("mode", ["js", "static"])
def test_live_two_pages(mode):
    recs = QuoteScraper(ScraperConfig(mode=mode, max_pages=2, delay=0.5)).run()
    assert len(recs) == 20
    assert {r["page"] for r in recs} == {1, 2}
    assert all(r["text"] and r["author"] for r in recs)
