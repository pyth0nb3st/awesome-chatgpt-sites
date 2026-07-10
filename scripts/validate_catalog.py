#!/usr/bin/env python3
"""Validate catalog structure without external Python dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "data" / "sites.json"
ALLOWED_CATEGORIES = {
    "Creative Tools",
    "Data Visualization",
    "Ecommerce and Storefronts",
    "Games",
    "Interactive Experiences",
    "Internal Apps and Dashboards",
    "Marketing Sites",
    "Education and Documentation",
}
PROVENANCE = {"official-source", "creator-submitted", "creator-confirmed", "source-link-only"}
PROMPT_LICENSES = {"CC0-1.0", "CC-BY-4.0", "creator-permission", "link-only"}
REVIEW_STATES = {"pending-human", "human-approved"}
REQUIRED = {
    "slug", "name", "live_url", "description", "category", "creator_name", "creator_url",
    "source_url", "prompt_url", "prompt_provenance", "prompt_license", "verified_on",
    "review_status", "reviewed_by_human", "source_checked", "live_checked", "status",
}
TRACKING_KEYS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "ref", "affiliate", "aff"}


def is_allowed_live_host(hostname: str | None) -> bool:
    return bool(hostname and (hostname == "openai.chatgpt.site" or hostname.endswith(".openai.chatgpt.site")))


def validate(records: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(records, list):
        return ["catalog: expected a JSON array"]

    seen_slugs: set[str] = set()
    seen_names: set[str] = set()
    seen_urls: set[str] = set()

    for index, record in enumerate(records):
        label = f"record {index}"
        if not isinstance(record, dict):
            errors.append(f"{label}: expected an object")
            continue
        label = f"record {index} ({record.get('slug', 'missing-slug')})"
        missing = REQUIRED - record.keys()
        extra = record.keys() - REQUIRED
        if missing:
            errors.append(f"{label}: missing fields: {', '.join(sorted(missing))}")
        if extra:
            errors.append(f"{label}: unexpected fields: {', '.join(sorted(extra))}")
        if missing:
            continue

        slug = record["slug"]
        name = record["name"]
        live_url = record["live_url"]
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            errors.append(f"{label}: slug must be a lowercase slug")
        elif slug in seen_slugs:
            errors.append(f"{label}: duplicate slug")
        seen_slugs.add(slug)

        folded_name = name.casefold() if isinstance(name, str) else ""
        if not name or not isinstance(name, str):
            errors.append(f"{label}: name must be a non-empty string")
        elif folded_name in seen_names:
            errors.append(f"{label}: duplicate name (case-insensitive)")
        seen_names.add(folded_name)

        parsed = urlparse(live_url) if isinstance(live_url, str) else urlparse("")
        if parsed.scheme != "https" or not is_allowed_live_host(parsed.hostname):
            errors.append(f"{label}: live_url must be HTTPS on an allowed hostname")
        if live_url in seen_urls:
            errors.append(f"{label}: duplicate live_url")
        seen_urls.add(live_url)
        query_keys = {key.casefold() for key, _ in parse_qsl(parsed.query, keep_blank_values=True)}
        if query_keys & TRACKING_KEYS:
            errors.append(f"{label}: live_url contains a tracking parameter")

        for field in ("source_url", "prompt_url"):
            value = record[field]
            if not isinstance(value, str) or urlparse(value).scheme != "https" or not urlparse(value).hostname:
                errors.append(f"{label}: {field} must be an absolute HTTPS URL")

        description = record["description"]
        if not isinstance(description, str) or not description or not description[0].isupper() or not description.endswith("."):
            errors.append(f"{label}: description must start uppercase and end with a period")
        if record["category"] not in ALLOWED_CATEGORIES:
            errors.append(f"{label}: unsupported category")
        if record["prompt_provenance"] not in PROVENANCE:
            errors.append(f"{label}: unsupported prompt_provenance")
        if record["prompt_license"] not in PROMPT_LICENSES:
            errors.append(f"{label}: unsupported prompt_license")
        if record["prompt_provenance"] == "source-link-only" and record["prompt_license"] != "link-only":
            errors.append(f"{label}: source-link-only provenance requires link-only rights")
        if record["review_status"] not in REVIEW_STATES:
            errors.append(f"{label}: unsupported review_status")
        if record["reviewed_by_human"] != (record["review_status"] == "human-approved"):
            errors.append(f"{label}: reviewed_by_human and review_status disagree")
        if record["source_checked"] is not True or record["live_checked"] is not True:
            errors.append(f"{label}: source_checked and live_checked must be true")
        if record["status"] != "active":
            errors.append(f"{label}: main catalog status must be active")
        try:
            date.fromisoformat(record["verified_on"])
        except (TypeError, ValueError):
            errors.append(f"{label}: verified_on must be an ISO date")

    if isinstance(records, list):
        expected = sorted(records, key=lambda item: (item.get("category", "").casefold(), item.get("name", "").casefold()) if isinstance(item, dict) else ("", ""))
        if records != expected:
            errors.append("catalog: entries must be sorted by category, then name")
    return errors


def load_catalog(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()
    try:
        records = load_catalog(args.path)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    errors = validate(records)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Catalog valid: {len(records)} entries")
    pending = sum(record["review_status"] == "pending-human" for record in records)
    if pending:
        print(f"Human review gate: {pending} entries pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
