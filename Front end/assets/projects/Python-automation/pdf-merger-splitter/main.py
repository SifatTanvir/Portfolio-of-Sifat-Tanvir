#!/usr/bin/env python3
"""Merge, split by page ranges, or rotate PDFs (pypdf)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def cmd_merge(inputs: list[Path], output: Path) -> None:
    w = PdfWriter()
    for p in inputs:
        if not p.is_file():
            print(f"Missing file: {p}", file=sys.stderr)
            sys.exit(1)
        r = PdfReader(str(p))
        for page in r.pages:
            w.add_page(page)
    w.write(output)
    print(f"Merged {len(inputs)} files -> {output.resolve()}")


def parse_ranges(spec: str, page_count: int) -> list[int]:
    """Spec like '1-2,5' → 0-based indices [0,1,4]."""
    indices: list[int] = []
    for part in spec.replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            start, end = int(a), int(b)
            if start < 1 or end < start:
                raise ValueError(f"Invalid range: {part}")
            for p in range(start, end + 1):
                if p > page_count:
                    break
                indices.append(p - 1)
        else:
            p = int(part)
            if p < 1 or p > page_count:
                raise ValueError(f"Page out of range: {p}")
            indices.append(p - 1)
    return indices


def cmd_split(input_pdf: Path, ranges: str, output: Path) -> None:
    r = PdfReader(str(input_pdf))
    n = len(r.pages)
    idxs = parse_ranges(ranges, n)
    w = PdfWriter()
    for i in idxs:
        w.add_page(r.pages[i])
    w.write(output)
    print(f"Extracted {len(idxs)} pages -> {output.resolve()}")


def cmd_rotate(input_pdf: Path, degrees: int, output: Path) -> None:
    r = PdfReader(str(input_pdf))
    w = PdfWriter()
    for page in r.pages:
        p = page
        p.rotate(degrees)
        w.add_page(p)
    w.write(output)
    print(f"Rotated {degrees} deg -> {output.resolve()}")


def cmd_demo(output_dir: Path) -> None:
    """Create two single-page PDFs and merge them (no user files required)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    a = output_dir / "demo_a.pdf"
    b = output_dir / "demo_b.pdf"
    merged = output_dir / "demo_merged.pdf"
    wa, wb = PdfWriter(), PdfWriter()
    wa.add_blank_page(width=200, height=200)
    wb.add_blank_page(width=200, height=200)
    wa.write(a)
    wb.write(b)
    cmd_merge([a, b], merged)


def main() -> None:
    ap = argparse.ArgumentParser(description="PDF merge / split / rotate")
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("merge", help="merge PDFs in order")
    m.add_argument("inputs", nargs="+", type=Path)
    m.add_argument("-o", "--output", type=Path, required=True)

    s = sub.add_parser("split", help="extract pages by 1-based ranges, e.g. 1-2,5")
    s.add_argument("input", type=Path)
    s.add_argument("--ranges", required=True)
    s.add_argument("-o", "--output", type=Path, required=True)

    rot = sub.add_parser("rotate", help="rotate all pages")
    rot.add_argument("input", type=Path)
    rot.add_argument("degrees", type=int, choices=(90, 180, 270))
    rot.add_argument("-o", "--output", type=Path, required=True)

    d = sub.add_parser("demo", help="write sample PDFs and merge")
    d.add_argument("--dir", type=Path, default=Path("pdf_demo_out"))

    args = ap.parse_args()
    if args.cmd == "merge":
        cmd_merge(args.inputs, args.output)
    elif args.cmd == "split":
        cmd_split(args.input, args.ranges, args.output)
    elif args.cmd == "rotate":
        cmd_rotate(args.input, args.degrees, args.output)
    elif args.cmd == "demo":
        cmd_demo(args.dir)


if __name__ == "__main__":
    main()
