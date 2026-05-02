#!/usr/bin/env python3
"""Sort files into subfolders by extension; optional duplicate detection (SHA-256)."""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

DEFAULT_MAP = {
    ".pdf": "PDFs",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".webp": "Images",
    ".mp4": "Videos",
    ".mov": "Videos",
    ".webm": "Videos",
    ".py": "Code",
    ".js": "Code",
    ".ts": "Code",
    ".html": "Code",
    ".css": "Code",
    ".json": "Code",
    ".txt": "Documents",
    ".md": "Documents",
}


def file_hash(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(description="Organize files by extension into folders.")
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--dest", type=Path, help="defaults to --source if omitted")
    ap.add_argument("--execute", action="store_true", help="actually move files (otherwise plan only)")
    ap.add_argument("--dedupe", action="store_true", help="skip files whose SHA-256 was already seen in dest")
    ap.add_argument("--date-subfolders", action="store_true", help="Images/PDFs/.../YYYY-MM under type folder")
    args = ap.parse_args()

    src = args.source
    dest_root = args.dest or src
    if not src.is_dir():
        print(f"Source not a directory: {src}", file=sys.stderr)
        sys.exit(1)

    seen_hashes: set[str] = set()
    plan: list[tuple[Path, Path]] = []

    for p in sorted(src.iterdir()):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        folder = DEFAULT_MAP.get(ext, "Other")
        if args.date_subfolders:
            from datetime import datetime

            m = datetime.fromtimestamp(p.stat().st_mtime)
            folder = str(Path(folder) / m.strftime("%Y-%m"))
        target_dir = dest_root / folder
        target = target_dir / p.name
        if args.dedupe:
            h = file_hash(p)
            if h in seen_hashes:
                print(f"dup-skip: {p.name}")
                continue
            seen_hashes.add(h)
        plan.append((p, target))

    for src_p, dst_p in plan:
        print(f"{src_p}  ->  {dst_p}")
        if args.execute:
            dst_p.parent.mkdir(parents=True, exist_ok=True)
            if dst_p.exists():
                print(f"  skip exists: {dst_p}", file=sys.stderr)
                continue
            shutil.move(str(src_p), str(dst_p))

    if not args.execute:
        print("\nDry run only. Pass --execute to move files.")


if __name__ == "__main__":
    main()
