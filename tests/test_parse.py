"""Offline parser test: renders a fixture with JS in a real Chromium page."""
from playwright.sync_api import sync_playwright
from quote_scraper.scraper import parse_page

HTML = """<html><body><div id=c></div>
<nav><ul class=pager><li class=next><a href="/js/page/2/">Next</a></li></ul></nav>
<script>
document.getElementById('c').innerHTML =
 '<div class="quote"><span class="text">\u201cHello\u201d</span>' +
 '<small class="author">Ada</small><a class="tag">code</a><a class="tag">ai</a></div>';
</script></body></html>"""


def test_parse_js_rendered_fixture():
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        page.set_content(HTML)
        recs, nxt = parse_page(page, 1, "https://quotes.toscrape.com/js/")
        b.close()
    assert recs == [{"text": "Hello", "author": "Ada", "tags": ["code", "ai"],
                     "page": 1, "source_url": "https://quotes.toscrape.com/js/"}]
    assert nxt == "https://quotes.toscrape.com/js/page/2/"
