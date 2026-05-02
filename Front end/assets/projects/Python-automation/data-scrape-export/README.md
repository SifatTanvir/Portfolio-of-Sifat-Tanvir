# Data scrape & export

**Default (safe):** parse the bundled sample HTML.

```bash
python data-scrape-export/main.py --html-file data-scrape-export/sample_job_listings.html --output jobs.csv
```

Excel:

```bash
python data-scrape-export/main.py --html-file data-scrape-export/sample_job_listings.html --output jobs.xlsx --excel
```

Optional remote fetch (your responsibility):

```bash
python data-scrape-export/main.py --url "https://example.com" --output out.csv
```
