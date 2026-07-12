#!/usr/bin/env python3
"""Report catalog/README drift without modifying either file."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CATALOG = ROOT / "data" / "sites.json"
PROMPT_ENTRY = re.compile(
    r"^- \[([^]]+)]\((https://[^)]+)\) - (.+), with "
    r"\[prompt and provenance]\((https://[^)]+)\)\.$"
)
UNAVAILABLE_ENTRY = re.compile(
    r"^- \[([^]]+)]\((https://[^)]+)\) - (.+\.) Prompt not publicly available\.$"
)


def parse_entry(line: str) -> tuple[str, str, str, str | None] | None:
    if match := PROMPT_ENTRY.fullmatch(line):
        name, live_url, description, prompt_url = match.groups()
        return name, live_url, f"{description}.", prompt_url
    if match := UNAVAILABLE_ENTRY.fullmatch(line):
        name, live_url, description = match.groups()
        return name, live_url, description, None
    return None


def main() -> int:
    records = json.loads(CATALOG.read_text(encoding="utf-8"))
    lines = README.read_text(encoding="utf-8").splitlines()
    parsed = [entry for line in lines if (entry := parse_entry(line))]
    errors: list[str] = []

    counts = Counter(url for _, url, _, _ in parsed)
    for url, count in counts.items():
        if count != 1:
            errors.append(f"README duplicate live URL ({count}): {url}")

    by_url = {url: (name, description, prompt_url) for name, url, description, prompt_url in parsed}
    catalog_urls = {record["live_url"] for record in records}
    for record in records:
        actual = by_url.get(record["live_url"])
        expected = (record["name"], record["description"], record["prompt_url"])
        if actual is None:
            errors.append(f"README missing: {record['live_url']}")
        elif actual != expected:
            errors.append(f"README mismatch for {record['slug']}: expected {expected!r}, got {actual!r}")
    for url in by_url.keys() - catalog_urls:
        errors.append(f"README URL missing from catalog: {url}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"README synchronized: {len(records)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
