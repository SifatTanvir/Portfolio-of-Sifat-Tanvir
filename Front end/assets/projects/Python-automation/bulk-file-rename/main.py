#!/usr/bin/env python3
"""Bulk rename files in a directory with prefix, suffix, counter, replace, strip spaces."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description="Bulk rename files (no directories).")
    ap.add_argument("--dir", type=Path, required=True)
    ap.add_argument("--glob", default="*", help="file glob, e.g. '*.jpg'")
    ap.add_argument("--prefix", default="")
    ap.add_argument("--suffix", default="")
    ap.add_argument("--replace", nargs=2, metavar=("FROM", "TO"), help="simple substring replace")
    ap.add_argument("--strip-spaces", action="store_true")
    ap.add_argument("--counter-start", type=int, default=1)
    ap.add_argument("--counter-width", type=int, default=3)
    ap.add_argument(
        "--serial",
        action="store_true",
        help="ignore stem; name as prefix + zero-padded counter + suffix + ext (e.g. vacation_001.jpg)",
    )
    ap.add_argument("--dry-run", action="store_true", help="print planned renames only")
    args = ap.parse_args()

    if not args.dir.is_dir():
        print(f"Not a directory: {args.dir}", file=sys.stderr)
        sys.exit(1)

    paths = sorted(p for p in args.dir.glob(args.glob) if p.is_file())
    if not paths:
        print("No files matched.")
        return

    n = args.counter_start
    for p in paths:
        ext = p.suffix
        if args.serial:
            num = str(n).zfill(args.counter_width)
            new_name = f"{args.prefix}{num}{args.suffix}{ext}"
        else:
            stem = p.stem
            if args.strip_spaces:
                stem = stem.replace(" ", "")
            if args.replace:
                stem = stem.replace(args.replace[0], args.replace[1])
            num = str(n).zfill(args.counter_width)
            new_name = f"{args.prefix}{stem}{args.suffix}{num}{ext}"
        dest = p.with_name(new_name)
        n += 1
        if dest == p:
            continue
        if dest.exists():
            print(f"Skip (exists): {dest.name}", file=sys.stderr)
            continue
        print(f"{p.name}  ->  {dest.name}")
        if not args.dry_run:
            p.rename(dest)


if __name__ == "__main__":
    main()
