# PDF merger & splitter

Bundled **sample inputs**: `samples/sample_a.pdf` and `samples/sample_b.pdf` (single-page PDFs). From the `Python-automation` root:

```bash
python pdf-merger-splitter/main.py merge pdf-merger-splitter/samples/sample_a.pdf pdf-merger-splitter/samples/sample_b.pdf -o merged_from_samples.pdf
```

```bash
# Built-in demo (creates PDFs then merges)
python pdf-merger-splitter/main.py demo --dir pdf_demo_out

# Merge
python pdf-merger-splitter/main.py merge a.pdf b.pdf -o merged.pdf

# Split (1-based page numbers)
python pdf-merger-splitter/main.py split merged.pdf --ranges 1-2 -o part.pdf

# Rotate all pages
python pdf-merger-splitter/main.py rotate merged.pdf 90 -o rotated.pdf
```

Requires `pypdf` from the root `requirements.txt`.
