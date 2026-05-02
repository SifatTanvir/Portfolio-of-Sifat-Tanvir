# Python automation toolkit

Runnable **Python 3.10+** command-line tools for common workflows: RLHF-style dataset prep, prompt benchmarking, ethical scraping demos, PDF utilities, bulk rename, file organization, scheduled email (SMTP), and URL validation.

## Setup

```bash
cd Python-automation
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Read **[LEGAL_AND_ETHICS.md](LEGAL_AND_ETHICS.md)** before using scraping or email features.

In the portfolio site, open **`projects.html`** and choose the **Python automation** tab for how to run each tool, download links, requirements, and expandable source for every `main.py`.

## Tools

| Folder | Purpose |
|--------|---------|
| [rlhf-dataset-builder](rlhf-dataset-builder/) | Import prompts → stub responses → rank → filter → JSONL export |
| [prompt-eval-pipeline](prompt-eval-pipeline/) | Compare stub “models” with latency/length/cost/heuristic scores |
| [data-scrape-export](data-scrape-export/) | Parse local sample HTML (optional URL with your own compliance) |
| [pdf-merger-splitter](pdf-merger-splitter/) | Merge, split by ranges, rotate PDFs |
| [bulk-file-rename](bulk-file-rename/) | Prefix, suffix, numbering, replace text |
| [file-organizer](file-organizer/) | Sort files by extension into folders |
| [auto-email-sender](auto-email-sender/) | JSON schedule + SMTP send or dry-run |
| [url-validation](url-validation/) | HTTP status, redirects, errors -> CSV |

## License

MIT — see [LICENSE](LICENSE) if present in the parent repository; otherwise follow your portfolio’s root license.
