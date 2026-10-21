"""Export scraped records to CSV / JSON."""
from __future__ import annotations

import csv
import json
from pathlib import Path

FIELDS = ["text", "author", "tags", "page", "source_url"]


def export_json(records: list[dict], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def export_csv(records: list[dict], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:  # BOM: Excel-friendly
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in records:
            row = dict(r)
            row["tags"] = "|".join(r.get("tags", []))
            writer.writerow({k: row.get(k, "") for k in FIELDS})
    return path


def export(records: list[dict], output_dir: str | Path, formats: list[str],
           stem: str = "quotes") -> list[Path]:
    out = Path(output_dir)
    written = []
    if "json" in formats:
        written.append(export_json(records, out / f"{stem}.json"))
    if "csv" in formats:
        written.append(export_csv(records, out / f"{stem}.csv"))
    return written
