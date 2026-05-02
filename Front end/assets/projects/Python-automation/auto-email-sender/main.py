#!/usr/bin/env python3
"""
Queue one-off scheduled emails (JSON on disk) and run a small daemon that sends when due.

Sending requires explicit --send and SMTP_* environment variables (no secrets in the repo).
Default daemon mode only prints what would be sent (dry run).
"""
from __future__ import annotations

import argparse
import json
import os
import smtplib
import ssl
import sys
import time
import uuid
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path


def _parse_local_dt(s: str) -> datetime:
    """Parse 'YYYY-MM-DD HH:MM' as local wall time, timezone-aware."""
    naive = datetime.strptime(s.strip(), "%Y-%m-%d %H:%M")
    return naive.astimezone()


def load(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, rows: list[dict]) -> None:
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def smtp_from_env() -> tuple[str, int, str, str, str]:
    host = os.environ.get("SMTP_HOST", "").strip()
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER", "").strip()
    password = os.environ.get("SMTP_PASSWORD", "")
    mail_from = os.environ.get("SMTP_FROM", user).strip()
    if not host or not user or not password or not mail_from:
        raise SystemExit(
            "Set SMTP_HOST, SMTP_USER, SMTP_PASSWORD, and SMTP_FROM (optional SMTP_PORT) to send."
        )
    return host, port, user, password, mail_from


def send_one(job: dict) -> None:
    host, port, user, password, mail_from = smtp_from_env()
    msg = EmailMessage()
    msg["Subject"] = job["subject"]
    msg["From"] = mail_from
    msg["To"] = ", ".join(job["to"])
    if job.get("cc"):
        msg["Cc"] = ", ".join(job["cc"])
    # Bcc recipients are still included in sendmail() rcpt list; omit header so addresses stay private.
    msg.set_content(job["body"])

    recipients = list(job["to"]) + list(job.get("cc") or []) + list(job.get("bcc") or [])
    context = ssl.create_default_context()
    with smtplib.SMTP(host, port, timeout=60) as server:
        server.ehlo()
        try:
            server.starttls(context=context)
            server.ehlo()
        except smtplib.SMTPException:
            pass
        server.login(user, password)
        server.sendmail(mail_from, recipients, msg.as_string())


def cmd_add(
    path: Path,
    to: list[str],
    cc: list[str],
    bcc: list[str],
    subject: str,
    body: str,
    at_local: str,
) -> None:
    rows = load(path)
    job = {
        "id": str(uuid.uuid4()),
        "to": to,
        "cc": cc,
        "bcc": bcc,
        "subject": subject,
        "body": body,
        "send_at": _parse_local_dt(at_local).astimezone(timezone.utc).isoformat(),
        "sent": False,
    }
    rows.append(job)
    save(path, rows)
    print(f"Queued job {job['id']} for UTC {job['send_at']} (stored in {path})")


def cmd_list(path: Path) -> None:
    rows = load(path)
    if not rows:
        print("No jobs.")
        return
    for j in rows:
        st = "sent" if j.get("sent") else "pending"
        print(f"{j['id'][:8]}..  {st}  at_utc={j['send_at']}  to={j['to']}  subj={j['subject'][:40]!r}")


def cmd_daemon(path: Path, interval: float, do_send: bool) -> None:
    print("Watching schedules. Ctrl+C to stop.")
    if not do_send:
        print("Dry run: prints when a job is due; does not send or modify the schedule file.")
    warned_due: set[str] = set()
    while True:
        now = datetime.now(timezone.utc)
        rows = load(path)
        changed = False
        for j in rows:
            if j.get("sent"):
                continue
            due = datetime.fromisoformat(j["send_at"])
            if due > now:
                continue
            jid = j["id"]
            if jid not in warned_due:
                print(f"Due: id={jid} to={j['to']} subject={j['subject']!r}")
                if not do_send:
                    print("  (dry run: start again with --send and SMTP_* env vars to send)")
                warned_due.add(jid)
            if do_send:
                try:
                    send_one(j)
                    j["sent"] = True
                    j["sent_at"] = now.isoformat()
                    changed = True
                    print("  Sent OK.")
                except Exception as e:
                    print(f"  Send failed: {e}", file=sys.stderr)
        if changed:
            save(path, rows)
        time.sleep(interval)


def main() -> None:
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument(
        "--file",
        type=Path,
        default=Path("email_schedules.json"),
        help="schedule JSON path (place before or after the subcommand)",
    )
    ap = argparse.ArgumentParser(description="Schedule emails via JSON + optional SMTP send.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", parents=[parent], help="append a scheduled job")
    a.add_argument("--to", action="append", required=True, help="repeat for multiple recipients")
    a.add_argument("--cc", action="append", default=None, help="repeatable")
    a.add_argument("--bcc", action="append", default=None, help="repeatable")
    a.add_argument("--subject", required=True)
    a.add_argument("--body", default="", help="plain text body (or use --body-file)")
    a.add_argument("--body-file", type=Path, help="read body from file")
    a.add_argument(
        "--at",
        dest="at_local",
        required=True,
        metavar="WHEN",
        help='local time "YYYY-MM-DD HH:MM" (this machine timezone)',
    )

    sub.add_parser("list", parents=[parent], help="list jobs")

    d = sub.add_parser("daemon", parents=[parent], help="poll file and send due jobs")
    d.add_argument("--interval", type=float, default=5.0)
    d.add_argument(
        "--send",
        action="store_true",
        help="actually send via SMTP (otherwise dry-run marks jobs sent when due)",
    )

    args = ap.parse_args()
    if args.cmd == "add":
        body = args.body
        if args.body_file:
            body = args.body_file.read_text(encoding="utf-8")
        cc = args.cc or []
        bcc = args.bcc or []
        cmd_add(args.file, args.to, cc, bcc, args.subject, body, args.at_local)
    elif args.cmd == "list":
        cmd_list(args.file)
    elif args.cmd == "daemon":
        cmd_daemon(args.file, args.interval, args.send)


if __name__ == "__main__":
    main()
