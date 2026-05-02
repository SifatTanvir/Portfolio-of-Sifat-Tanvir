#!/usr/bin/env python3
"""Check URLs for HTTP status and final URL after redirects; export CSV (stdlib only)."""
from __future__ import annotations

import argparse
import csv
import sys
import urllib.error
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (compatible; PortfolioURLCheck/1.0; educational)"


def check_url(url: str, timeout: float) -> tuple[int, str, str]:
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())

    def head() -> tuple[int, str]:
        req = urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD")
        resp = opener.open(req, timeout=timeout)
        try:
            return resp.getcode(), resp.geturl()
        finally:
            resp.close()

    def get() -> tuple[int, str]:
        req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
        resp = opener.open(req, timeout=timeout)
        try:
            return resp.getcode(), resp.geturl()
        finally:
            resp.close()

    try:
        code, final = head()
        return code, final, ""
    except urllib.error.HTTPError as e:
        if e.code == 405:
            try:
                code, final = get()
                return code, final, ""
            except Exception as e2:
                return 0, url, f"GET after 405 failed: {e2!r}"
        return e.code, getattr(e, "url", url) or url, ""
    except urllib.error.URLError as e:
        return 0, url, str(e.reason)
    except Exception as e:
        return 0, url, repr(e)


def read_urls(path: Path | None, inline: list[str]) -> list[str]:
    rows: list[str] = []
    if path:
        for line in path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if "," in s and not s.lower().startswith("http"):
                s = s.split(",", 1)[0].strip()
            rows.append(s)
    rows.extend(u.strip() for u in inline if u.strip())
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate URLs; write CSV url,status,final_url,error")
    ap.add_argument("--input", type=Path, help="text file: one URL per line (optional CSV first column)")
    ap.add_argument("--url", action="append", default=[], help="repeat for single URLs")
    ap.add_argument("-o", "--output", type=Path, default=Path("url_check_results.csv"))
    ap.add_argument("--timeout", type=float, default=15.0)
    args = ap.parse_args()

    urls = read_urls(args.input, args.url)
    if not urls:
        print("Provide --input file and/or one or more --url values.", file=sys.stderr)
        sys.exit(1)

    out_rows: list[dict[str, str]] = []
    for u in urls:
        code, final, err = check_url(u, args.timeout)
        redirects = "yes" if code and final.rstrip("/") != u.rstrip("/") else "no"
        out_rows.append(
            {
                "url": u,
                "status": str(code),
                "final_url": final,
                "redirect": redirects,
                "error": err,
            }
        )
        print(f"{u}  {code}  {final}")

    with args.output.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["url", "status", "final_url", "redirect", "error"])
        w.writeheader()
        w.writerows(out_rows)
    print(f"Wrote {len(out_rows)} rows -> {args.output.resolve()}")


if __name__ == "__main__":
    main()
