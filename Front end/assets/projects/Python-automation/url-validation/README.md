# URL validation

Checks each URL with `HEAD` (falls back to `GET` if the server rejects `HEAD`). Writes CSV columns: `url`, `status`, `final_url`, `redirect`, `error`.

```bash
python url-validation/main.py --input url-validation/sample_urls.txt -o url_results.csv
python url-validation/main.py --url https://example.com --url https://example.invalid
```

Only request sites you are allowed to probe. Default timeout is 15 seconds per URL.
