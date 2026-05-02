#!/usr/bin/env python3
"""
Prompt evaluation pipeline: run each prompt through stub "models", collect metrics, export CSV.

Metrics: response length, latency (simulated), heuristic cost, relevance (token overlap),
hallucination heuristic (forbidden absolute claims).
"""
from __future__ import annotations

import argparse
import csv
import random
import re
import time
from pathlib import Path


def stub_model(name: str, prompt: str) -> tuple[str, float]:
    """Return (text, simulated_latency_seconds)."""
    rng = random.Random(hash((name, prompt)) % (2**32))
    t0 = time.perf_counter()
    noise = rng.randint(8, 80)
    body = f"[{name}] " + " ".join(prompt.split()[:12]) + " … " + ("x" * noise)
    time.sleep(0.008 + rng.random() * 0.04)  # small real delay so runs feel "live"
    latency = time.perf_counter() - t0
    return body, latency


def relevance(prompt: str, response: str) -> float:
    ps = set(re.findall(r"[a-z0-9]+", prompt.lower()))
    rs = set(re.findall(r"[a-z0-9]+", response.lower()))
    if not ps:
        return 0.0
    return round(len(ps & rs) / len(ps), 3)


def hallucination_score(response: str) -> float:
    """Higher = more suspicious absolute claims (demo heuristic)."""
    bad = re.compile(
        r"\b(always|never|100% guaranteed|cure for cancer|official truth)\b",
        re.I,
    )
    return min(1.0, len(bad.findall(response)) * 0.33)


def cost_estimate(tokens: int, usd_per_1k: float = 0.002) -> float:
    return round((tokens / 1000.0) * usd_per_1k, 6)


def main() -> None:
    ap = argparse.ArgumentParser(description="Benchmark prompts across stub models.")
    ap.add_argument("--input", type=Path, required=True, help="One prompt per line .txt")
    ap.add_argument("--output", type=Path, default=Path("eval_results.csv"))
    args = ap.parse_args()

    prompts = [ln.strip() for ln in args.input.read_text(encoding="utf-8").splitlines() if ln.strip()]
    models = ["model_a", "model_b", "model_c"]
    if not prompts:
        args.output.write_text("", encoding="utf-8")
        print("No prompts in input; wrote empty CSV.")
        return

    rows: list[dict[str, object]] = []
    for p in prompts:
        for m in models:
            text, lat = stub_model(m, p)
            toks = max(1, len(text.split()))
            rows.append(
                {
                    "prompt": p,
                    "model": m,
                    "response_length": len(text),
                    "latency_sec": round(lat, 4),
                    "cost_estimate_usd": cost_estimate(toks),
                    "relevance": relevance(p, text),
                    "hallucination_score": hallucination_score(text),
                    "response_preview": text[:200].replace("\n", " "),
                }
            )

    with args.output.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            w.writeheader()
            w.writerows(rows)

    print(f"Wrote {len(rows)} rows -> {args.output.resolve()}")


if __name__ == "__main__":
    main()
