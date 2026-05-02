# Prompt evaluation pipeline

```bash
python prompt-eval-pipeline/main.py --input prompt-eval-pipeline/sample_prompts.txt --output eval.csv
```

Outputs one row per (prompt, model) with length, latency, heuristic cost, relevance, and hallucination score. Swap `stub_model()` for real API calls you are authorized to use.
