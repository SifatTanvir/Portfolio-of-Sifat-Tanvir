# Auto email sender

Stores jobs in a JSON file (default `email_schedules.json` in the current working directory). A small daemon checks the clock every few seconds and sends due messages when you pass **`--send`** and configure SMTP via environment variables (never commit secrets).

**Sample queue:** `sample_queue.json` contains one far-future pending job so you can run `list` or a dry-run `daemon` without affecting a real queue.

```bash
# Queue a job (local wall time on this PC)
python auto-email-sender/main.py add --to you@example.com --subject "Hello" --body "Test" --at "2026-05-03 14:30"

python auto-email-sender/main.py list --file auto-email-sender/sample_queue.json

python auto-email-sender/main.py list --file email_schedules.json

# Dry run: prints when a job is due; does not send or edit the file
python auto-email-sender/main.py daemon --file email_schedules.json --interval 5

# Real send (set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM)
python auto-email-sender/main.py daemon --file email_schedules.json --send
```

Optional body from file: `--body-file message.txt`. Repeat `--to` / `--cc` / `--bcc` for multiple addresses.

See `../LEGAL_AND_ETHICS.md` for acceptable use (consent, anti-spam, provider terms).
