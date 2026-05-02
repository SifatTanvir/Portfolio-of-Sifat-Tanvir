#!/usr/bin/env python3
"""
Parse HTML (local file by default) and export rows to CSV or Excel.

Default path uses the bundled sample. For --url, you must have rights to fetch
that content and comply with robots.txt / terms of service (see LEGAL_AND_ETHICS.md).
"""
from __future__ import annotations

import argparse
import csv
import sys
import urllib.error
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

USER_AGENT = "PythonAutomationPortfolio/1.0 (+https://example.local; educational)"


def parse_jobs(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    rows: list[dict[str, str]] = []
    for card in soup.select("article.job-card"):
        title_el = card.select_one(".title")
        company_el = card.select_one(".company")
        loc_el = card.select_one(".location")
        rows.append(
            {
                "title": title_el.get_text(strip=True) if title_el else "",
                "company": company_el.get_text(strip=True) if company_el else "",
                "location": loc_el.get_text(strip=True) if loc_el else "",
            }
        )
    return rows


def fetch_url(url: str, timeout: float = 15.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def main() -> None:
    ap = argparse.ArgumentParser(description="Scrape job-like cards from HTML → CSV/Excel.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--html-file", type=Path, help="Local .html file (recommended default)")
    src.add_argument("--url", type=str, help="HTTP(S) URL — only use sites you are allowed to access")
    ap.add_argument("--output", type=Path, default=Path("scraped.csv"))
    ap.add_argument("--excel", action="store_true", help="write .xlsx instead of .csv (needs pandas+openpyxl)")
    args = ap.parse_args()

    if args.html_file:
        if not args.html_file.is_file():
            print(f"File not found: {args.html_file}", file=sys.stderr)
            sys.exit(1)
        html = args.html_file.read_text(encoding="utf-8")
    else:
        print("Fetching remote URL — ensure you have permission.", file=sys.stderr)
        try:
            html = fetch_url(args.url)
        except urllib.error.URLError as e:
            print(f"Fetch failed: {e}", file=sys.stderr)
            sys.exit(1)

    rows = parse_jobs(html)
    if not rows:
        print("No matching .job-card entries found.", file=sys.stderr)
        sys.exit(2)

    out = args.output
    if args.excel:
        import pandas as pd

        if not str(out).lower().endswith(".xlsx"):
            out = out.with_suffix(".xlsx")
        pd.DataFrame(rows).to_excel(out, index=False)
    else:
        if not str(out).lower().endswith(".csv"):
            out = out.with_suffix(".csv")
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    print(f"Wrote {len(rows)} rows -> {out.resolve()}")


if __name__ == "__main__":
    main()
