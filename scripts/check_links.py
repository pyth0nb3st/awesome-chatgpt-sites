#!/usr/bin/env python3
"""Check status and redirects without saving or parsing response bodies."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "sites.json"
USER_AGENT = "awesome-chatgpt-sites/0.1 (+https://github.com/pyth0nb3st/awesome-chatgpt-sites)"


def allowed_host(hostname: str | None) -> bool:
    return bool(hostname and hostname != "chatgpt.site" and hostname.endswith(".chatgpt.site"))


def changed_urls(records: list[dict[str, object]]) -> list[str]:
    base_ref = os.environ.get("GITHUB_BASE_REF")
    command = ["git", "diff", "--unified=0"]
    if base_ref:
        command.append(f"origin/{base_ref}")
    command.extend(["--", "data/sites.json"])
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    found = set(re.findall(r'^\+\s*"live_url":\s*"(https://[^"]+)"', result.stdout, re.MULTILINE))
    return [record["live_url"] for record in records if record["live_url"] in found] or [record["live_url"] for record in records]


def request_headers(url: str, method: str, timeout: float) -> tuple[int, str]:
    request = Request(url, method=method, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urlopen(request, timeout=timeout) as response:
        return response.status, response.geturl()


def check(url: str, timeout: float, retries: int) -> tuple[str, int | None, str, str | None]:
    last_error: str | None = None
    for attempt in range(retries + 1):
        for method in ("HEAD", "GET"):
            try:
                status, final_url = request_headers(url, method, timeout)
                if not 200 <= status <= 399:
                    return url, status, final_url, f"HTTP {status}"
                if not allowed_host(urlparse(final_url).hostname):
                    return url, status, final_url, "redirected to an unrelated hostname"
                return url, status, final_url, None
            except HTTPError as exc:
                if method == "HEAD" and exc.code in {403, 405, 501}:
                    continue
                last_error = f"HTTP {exc.code}"
                if 400 <= exc.code < 500:
                    return url, exc.code, exc.geturl(), last_error
                break
            except (URLError, TimeoutError, OSError) as exc:
                last_error = str(exc)
                if method == "HEAD":
                    continue
                break
        if attempt < retries:
            time.sleep(0.25 * (attempt + 1))
    return url, None, url, last_error or "request failed"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--changed-only", action="store_true")
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--retries", type=int, default=2, choices=range(0, 3))
    parser.add_argument("--workers", type=int, default=4, choices=range(1, 5))
    args = parser.parse_args()

    records = json.loads(CATALOG.read_text(encoding="utf-8"))
    urls = changed_urls(records) if args.changed_only else [record["live_url"] for record in records]
    failures = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(check, url, args.timeout, args.retries) for url in urls]
        for future in as_completed(futures):
            url, status, final_url, error = future.result()
            if error:
                failures += 1
                print(f"FAIL\t{url}\t{status or '-'}\t{final_url}\t{error}")
            else:
                print(f"OK\t{url}\t{status}\t{final_url}")
    print(f"Checked {len(urls)} URL(s); {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
