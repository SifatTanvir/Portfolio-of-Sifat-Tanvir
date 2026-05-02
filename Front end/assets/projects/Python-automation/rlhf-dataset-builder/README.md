# RLHF dataset builder

**Workflow:** Raw prompts → generate responses → (optional human ranks CSV) → toxicity / duplicate filter → JSONL export.

## Run (from `Python-automation` root)

```bash
python rlhf-dataset-builder/main.py --input rlhf-dataset-builder/sample_prompts.csv --output out.jsonl
```

Optional ranks file `ranks.csv`:

```csv
prompt_hash,winner
a1b2c3d4e5f67890,1
```

`prompt_hash` is printed in each record’s `meta` after a run, or compute SHA256 of normalized prompt (see `main.py`).

## Notes

- Default responses are **deterministic stubs** so the pipeline runs offline with no API keys.
- Replace `gen_responses()` with calls to **your** model endpoint only under compliant terms.
