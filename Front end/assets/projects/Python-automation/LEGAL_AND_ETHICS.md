# Legal and ethical use

These scripts are for **education and automation you control**. Before publishing or running in production:

1. **Web scraping** — Only scrape sites you **own** or have **written permission** to access. Respect `robots.txt`, terms of service, and applicable law. The sample scraper defaults to a **local HTML file** bundled in this repo.
2. **Email** — Do not send unsolicited mail. Use real SMTP credentials you control. The scheduler supports **dry-run** mode so you can test without sending.
3. **RLHF / model outputs** — If you plug in external APIs (e.g. OpenAI-compatible endpoints), you are responsible for API terms, data retention, and **not** submitting personal data you are not allowed to process.
4. **File operations** — Bulk rename and organizer can move or overwrite files. Use `--dry-run` first where supported.

This project is provided as-is without warranty.
