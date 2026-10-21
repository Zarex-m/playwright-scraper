import csv, json
import pytest
from quote_scraper.config import ScraperConfig
from quote_scraper.exporters import export
from quote_scraper.cli import build_parser, make_config

REC = [{"text": "你好 world", "author": "A", "tags": ["x", "y"], "page": 1, "source_url": "u"}]


def test_start_url():
    assert ScraperConfig(mode="js").start_url.endswith("/js/")
    assert ScraperConfig(mode="static").start_url.endswith(".com/")


def test_validate_rejects_bad_mode():
    with pytest.raises(ValueError):
        ScraperConfig(mode="nope").validate()


def test_config_file_and_cli_override(tmp_path):
    f = tmp_path / "c.json"; f.write_text(json.dumps({"delay": 5, "max_pages": 2}))
    cfg = make_config(build_parser().parse_args(["--config", str(f), "--max-pages", "4"]))
    assert cfg.delay == 5 and cfg.max_pages == 4


def test_unknown_config_key(tmp_path):
    f = tmp_path / "c.json"; f.write_text('{"bogus": 1}')
    with pytest.raises(ValueError):
        ScraperConfig.from_file(f)


def test_export_csv_json(tmp_path):
    paths = export(REC, tmp_path, ["csv", "json"])
    assert len(paths) == 2
    assert json.loads((tmp_path / "quotes.json").read_text("utf-8"))[0]["text"] == "你好 world"
    rows = list(csv.DictReader((tmp_path / "quotes.csv").open(encoding="utf-8-sig")))
    assert rows[0]["tags"] == "x|y"
