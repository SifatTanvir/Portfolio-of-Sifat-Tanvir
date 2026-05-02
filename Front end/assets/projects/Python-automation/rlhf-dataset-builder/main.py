#!/usr/bin/env python3
"""
RLHF-style dataset builder (stub generators for local, ethical demos).

Workflow: Raw prompts → generate responses → optional ranks → quality filter → export JSONL.

Replace stub generators with your own API calls only where you have rights and API terms allow it.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

# Minimal demo blocklist — extend with care; not a production moderation model
TOXIC_WORDS = frozenset({"kill", "terror", "bomb"})


def norm_prompt(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(norm_prompt(prompt).encode("utf-8")).hexdigest()[:16]


def toxic_score(text: str) -> float:
    low = text.lower()
    hits = sum(1 for w in TOXIC_WORDS if w in low)
    return min(1.0, hits * 0.35)


def load_prompts(path: Path) -> list[str]:
    suf = path.suffix.lower()
    if suf == ".csv":
        out: list[str] = []
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError("CSV has no header row")
            key = "prompt" if "prompt" in reader.fieldnames else ("text" if "text" in reader.fieldnames else reader.fieldnames[0])
            for row in reader:
                p = (row.get(key) or "").strip()
                if p:
                    out.append(p)
        return out
    if suf == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("JSON must be a list of strings or objects with 'prompt'")
        rows: list[str] = []
        for item in data:
            if isinstance(item, str):
                rows.append(item.strip())
            elif isinstance(item, dict) and item.get("prompt"):
                rows.append(str(item["prompt"]).strip())
        return [x for x in rows if x]
    if suf == ".txt":
        return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    raise ValueError("Supported inputs: .csv (column prompt|text), .json list, .txt lines")


def gen_responses(prompt: str, n: int) -> list[str]:
    """Deterministic stub 'model' outputs — swap for real inference under your policies."""
    h = int(hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:6], 16)
    base = prompt.strip()[:200]
    templates = [
        "Concise take: {base} (focus: correctness, stub-{h}).",
        "Alternate phrasing: {base} — emphasizes clarity over brevity [{h}].",
        "Step-by-step style: break down: {base} (outline only, stub-{h}).",
    ]
    return [t.format(base=base, h=h % 9999) for t in templates[:n]]


def load_ranks(path: Path) -> dict[str, int]:
    m: dict[str, int] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ph = (row.get("prompt_hash") or "").strip()
            w = row.get("winner")
            if ph and w is not None and str(w).strip() != "":
                m[ph] = int(w)
    return m


def main() -> None:
    ap = argparse.ArgumentParser(description="Build JSONL preference dataset from prompts (stub responses).")
    ap.add_argument("--input", type=Path, required=True, help="prompts.csv | prompts.json | prompts.txt")
    ap.add_argument("--output", type=Path, default=Path("dataset.jsonl"))
    ap.add_argument("--responses", type=int, default=3, help="stub responses per prompt")
    ap.add_argument("--ranks", type=Path, help="CSV: prompt_hash,winner (0-based index)")
    ap.add_argument("--max-toxic", type=float, default=0.5, help="drop if all responses exceed this toxicity score")
    args = ap.parse_args()

    if not args.input.is_file():
        print(f"Input not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    raw = load_prompts(args.input)
    seen: set[str] = set()
    prompts: list[str] = []
    for p in raw:
        k = norm_prompt(p)
        if not k or k in seen:
            continue
        seen.add(k)
        prompts.append(p)

    ranks = load_ranks(args.ranks) if args.ranks and args.ranks.is_file() else {}

    lines: list[str] = []
    for p in prompts:
        ph = prompt_hash(p)
        responses = gen_responses(p, max(2, min(5, args.responses)))
        scores = [toxic_score(r) for r in responses]
        viable = [i for i, s in enumerate(scores) if s <= args.max_toxic]
        if not viable:
            continue
        winner = ranks.get(ph)
        if winner is not None and (winner < 0 or winner >= len(responses)):
            winner = None
        if winner is None or winner not in viable:
            winner = min(viable, key=lambda i: scores[i])
        losers = [i for i in viable if i != winner]
        rejected = responses[losers[0]] if losers else responses[(winner + 1) % len(responses)]
        rec = {
            "prompt": p,
            "chosen": responses[winner],
            "rejected": rejected,
            "meta": {"prompt_hash": ph, "toxicity_chosen": scores[winner], "dupes_removed": len(raw) - len(prompts)},
        }
        lines.append(json.dumps(rec, ensure_ascii=False))

    args.output.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    print(f"Wrote {len(lines)} JSONL records -> {args.output.resolve()}")


if __name__ == "__main__":
    main()
