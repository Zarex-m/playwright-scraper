"""Command-line entry point."""
from __future__ import annotations

import argparse
import logging
import sys

from .config import ScraperConfig
from .exporters import export
from .scraper import QuoteScraper


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="quote-scraper",
                                description="Scrape quotes.toscrape.com with Playwright.")
    p.add_argument("--config", help="Path to JSON config file")
    p.add_argument("--mode", choices=["js", "static"], help="JS-rendered (/js/) or static pages")
    p.add_argument("--max-pages", type=int, help="Max pages to crawl (0 = all)")
    p.add_argument("--delay", type=float, help="Seconds between requests")
    p.add_argument("--retries", type=int, help="Retries per page")
    p.add_argument("--output-dir", help="Directory for exported files")
    p.add_argument("--format", dest="formats", action="append", choices=["csv", "json"],
                   help="Export format (repeatable, default csv+json)")
    p.add_argument("--headed", action="store_true", help="Show the browser window")
    p.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    p.add_argument("--log-file", help="Also write logs to this file")
    return p


def setup_logging(level: str, log_file: str | None) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(level=level, handlers=handlers, force=True,
                        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")


def make_config(args: argparse.Namespace) -> ScraperConfig:
    base = ScraperConfig.from_file(args.config) if args.config else ScraperConfig()
    cfg = base.merge(mode=args.mode, max_pages=args.max_pages, delay=args.delay,
                     retries=args.retries, output_dir=args.output_dir, formats=args.formats,
                     headless=False if args.headed else None)
    cfg.validate()
    return cfg


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    setup_logging(args.log_level, args.log_file)
    try:
        cfg = make_config(args)
        records = QuoteScraper(cfg).run()
        for path in export(records, cfg.output_dir, cfg.formats):
            logging.info("Wrote %s", path)
    except Exception as exc:  # top-level guard for a clean exit code
        logging.exception("Scrape failed: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
