# Bulk file rename

Bundled **sample inputs**: `sample_in/` contains three `.txt` files (including one with a space in the name) for dry-run experiments from the `Python-automation` root, e.g. `--dir bulk-file-rename/sample_in --glob "*.txt" …`.

Serial names (`img1.jpg` -> `vacation_001.jpg` style):

```powershell
mkdir demo_rename; ni demo_rename/img1.jpg -ItemType File; ni demo_rename/img2.jpg -ItemType File
python bulk-file-rename/main.py --dir demo_rename --glob "*.jpg" --serial --prefix vacation_ --counter-width 3 --dry-run
python bulk-file-rename/main.py --dir demo_rename --glob "*.jpg" --serial --prefix vacation_ --counter-width 3
```

Stem mode (keeps original stem, adds prefix/suffix/counter): omit `--serial`. Options: `--suffix`, `--replace FROM TO`, `--strip-spaces`, `--counter-start`, `--counter-width`.
