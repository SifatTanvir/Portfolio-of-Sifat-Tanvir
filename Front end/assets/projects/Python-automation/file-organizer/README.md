# File organizer

Bundled **sample inputs**: `sample_messy_in/` has mixed extensions (`.txt`, `.py`, `.md`, `.json`) for a dry run from the `Python-automation` root:

```bash
python file-organizer/main.py --source file-organizer/sample_messy_in --dest ./organizer_demo_out
python file-organizer/main.py --source file-organizer/sample_messy_in --dest ./organizer_demo_out --execute
```

```bash
python file-organizer/main.py --source ./messy_folder --dest ./organized --execute
```

Dry run (default without `--execute`) prints the planned moves. Flags: `--dedupe`, `--date-subfolders`.
