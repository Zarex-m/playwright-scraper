"""Configuration: defaults < JSON config file < CLI args."""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict, fields
from pathlib import Path


@dataclass
class ScraperConfig:
    base_url: str = "https://quotes.toscrape.com"
    mode: str = "js"  # "js" -> /js/ (client-rendered), "static" -> /
    max_pages: int = 0  # 0 = follow pagination until the end
    delay: float = 1.0  # seconds between page requests (rate limit)
    retries: int = 3
    backoff: float = 2.0  # exponential backoff base, seconds
    timeout_ms: int = 15000
    headless: bool = True
    output_dir: str = "output"
    formats: list[str] = field(default_factory=lambda: ["csv", "json"])
    user_agent: str = "Mozilla/5.0 (portfolio-scraper; +https://github.com/Zarex-m)"

    @property
    def start_url(self) -> str:
        path = "/js/" if self.mode == "js" else "/"
        return self.base_url.rstrip("/") + path

    @classmethod
    def from_file(cls, path: str | Path) -> "ScraperConfig":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        known = {f.name for f in fields(cls)}
        unknown = set(data) - known
        if unknown:
            raise ValueError(f"Unknown config keys: {sorted(unknown)}")
        return cls(**data)

    def merge(self, **overrides) -> "ScraperConfig":
        data = asdict(self)
        data.update({k: v for k, v in overrides.items() if v is not None})
        return ScraperConfig(**data)

    def validate(self) -> None:
        if self.mode not in {"js", "static"}:
            raise ValueError("mode must be 'js' or 'static'")
        if self.max_pages < 0 or self.retries < 0 or self.delay < 0:
            raise ValueError("max_pages, retries and delay must be >= 0")
        bad = set(self.formats) - {"csv", "json"}
        if bad:
            raise ValueError(f"Unsupported formats: {sorted(bad)}")
