# PDF Markdown Cleaner

[![CI](https://img.shields.io/github/actions/workflow/status/phuchung/pdf-md-cleaner/ci.yml?label=CI)](../../actions)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-1.0.0-informational)](../../releases)
[![License](https://img.shields.io/badge/license-MIT-green)](../LICENSE)
[![Platform](<https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey>)](#supported-platforms)

# PDF Markdown Cleaner

PDF Markdown Cleaner is a document-processing pipeline for converting scanned and text-based PDF documents into clean, structured, publication-ready Markdown.

It is designed for documents where ordinary PDF-to-text extraction is not sufficient, particularly **government manuals, legislation, rules, audit documents, schedules, annexures, registers, and statutory forms**.

The pipeline combines native PDF extraction, high-resolution page rendering, image preprocessing, OCR, structural reconstruction, table extraction, OCR cleanup, and Markdown generation.

## What problem does it solve?

A normal PDF extractor often produces output like:

```text
Section 19 Audit of accounts
of local bodies shall be...
Page 23
GOVERNMENT OF SIKKIM
23
accounts
...
```

That output is technically extractable but unsuitable for publication.

PDF Markdown Cleaner instead aims to produce:

```markdown
## Section 19 — Audit of Accounts

The accounts of local bodies shall be audited
in accordance with the provisions of this Act.

### Table of Contents

* **Section 19 — Audit of Accounts** ........ Page 23
```

The system preserves document structure while removing common scanning and OCR artifacts.

## Core capabilities

| Capability            | Description                                               |
| --------------------- | --------------------------------------------------------- |
| PDF rendering         | Converts every source page into a high-resolution image   |
| OCR                   | Uses Tesseract for scanned documents                      |
| Image preprocessing   | Denoising, grayscale conversion and adaptive thresholding |
| Text extraction       | Supports native PDF text where available                  |
| Table extraction      | Uses`pdfplumber` for structured tables                  |
| OCR repair            | Corrects common OCR and formatting artifacts              |
| Header/footer removal | Detects repeated running headers and footers              |
| Page references       | Maintains original scanned page references                |
| Heading detection     | Identifies chapters, sections, rules, schedules and forms |
| Form cleanup          | Converts noisy form lines into clean Markdown fields      |
| Markdown generation   | Produces GitHub-compatible Markdown                       |
| TOC generation        | Builds a document-level table of contents                 |
| Cross-platform        | Supports Windows, macOS and Linux                         |

## Architecture

```text
                         ┌───────────────────┐
                         │     Source PDF    │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   PDF Renderer    │
                         │     PyMuPDF       │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Image Preprocessor│
                         │ OpenCV + Pillow   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    OCR Engine     │
                         │    Tesseract      │
                         └─────────┬─────────┘
                                   │
                 ┌─────────────────┴──────────────────┐
                 │                                    │
                 ▼                                    ▼
       ┌───────────────────┐                ┌───────────────────┐
       │ Text Processing   │                │ Table Extraction  │
       │ OCR Repair        │                │    pdfplumber     │
       └─────────┬─────────┘                └─────────┬─────────┘
                 │                                    │
                 └────────────────┬───────────────────┘
                                  ▼
                         ┌───────────────────┐
                         │ Structure Analysis│
                         │ Headings / Rules  │
                         │ Forms / Schedules │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Markdown Generator│
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   document.md     │
                         └───────────────────┘
```

## Extraction strategy

The project deliberately uses different techniques for different PDF components.

| Document component | Primary method           | Reason                           |
| ------------------ | ------------------------ | -------------------------------- |
| Native PDF text    | PyMuPDF                  | Fast and preserves existing text |
| Scanned pages      | Tesseract OCR            | Handles image-only PDFs          |
| Tables             | pdfplumber               | Better structured extraction     |
| Page images        | PyMuPDF                  | Reliable PDF rendering           |
| Image cleanup      | OpenCV                   | Removes noise and improves OCR   |
| Forms              | OCR + structural cleanup | Preserves fields and blanks      |
| Headings           | Pattern analysis         | Reconstructs document hierarchy  |
| TOC                | Structural analysis      | Generates searchable navigation  |

## Old workflow vs PDF Markdown Cleaner

| Area             | Manual transcription | Basic PDF extraction | PDF Markdown Cleaner   |
| ---------------- | -------------------- | -------------------- | ---------------------- |
| Scanned PDFs     | Poor                 | Usually fails        | Supported              |
| OCR              | Manual               | Limited              | Tesseract              |
| Tables           | Manual               | Often corrupted      | Structured extraction  |
| Page references  | Manual               | Frequently lost      | Preserved              |
| Headers/footers  | Manual cleanup       | Usually retained     | Automatically filtered |
| Legal headings   | Manual               | Flattened            | Reconstructed          |
| Forms            | Manual               | Poor                 | Field cleanup          |
| Markdown         | Manual               | Requires conversion  | Native output          |
| Reproducibility  | Low                  | Medium               | High                   |
| Batch processing | Difficult            | Good                 | Designed for it        |
| Cross-platform   | Human-dependent      | Varies               | Windows/macOS/Linux    |

## Project structure

```text
pdf-md-cleaner/
│
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .gitignore
│
├── src/
│   └── pdf_md_cleaner/
│       ├── __init__.py
│       ├── cli.py
│       ├── ocr.py
│       ├── preprocessing.py
│       ├── extraction.py
│       ├── tables.py
│       ├── structure.py
│       ├── cleanup.py
│       └── markdown.py
│
├── tests/
│   ├── test_ocr.py
│   ├── test_cleanup.py
│   ├── test_tables.py
│   └── test_markdown.py
│
├── input/
│   └── source.pdf
│
├── output/
│   └── document.md
│
├── work/
│   └── pages/
│
└── docs/
    ├── SETUP.md
    └── TROUBLESHOOTING.md
```

## Quickstart

### 1. Install prerequisites

See [docs/SETUP.md](docs/SETUP.md).

### 2. Create the environment

Linux/macOS:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Verify OCR

```bash
tesseract --version
```

### 4. Process a PDF

```bash
python legal_pdf_to_markdown.py input/document.pdf -o output/document.md
```

### 5. Use higher OCR resolution

```bash
python legal_pdf_to_markdown.py input/document.pdf \
    -o output/document.md \
    --dpi 400
```

Windows PowerShell:

```powershell
python legal_pdf_to_markdown.py input\document.pdf `
    -o output\document.md `
    --dpi 400
```

### 6. Review the generated Markdown

Open:

```text
output/document.md
```

For setup problems, see [docs/SETUP.md](docs/SETUP.md).

For extraction and OCR problems, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

## Recommended processing workflow

For important legal or archival documents:

```text
SOURCE PDF
   ↓
Backup original
   ↓
Run extraction
   ↓
Inspect OCR output
   ↓
Inspect tables/forms
   ↓
Compare against source pages
   ↓
Correct verified errors
   ↓
Run Markdown validation
   ↓
Publish
```

Do not treat OCR output as legally authoritative without comparing it against the scanned source.

## Performance guidance

| Document              | Recommended DPI | Expected priority         |
| --------------------- | --------------: | ------------------------- |
| Clean digital PDF     |        200–300 | Speed                     |
| Good scanned document |             300 | Balanced                  |
| Old government scan   |        300–400 | Accuracy                  |
| Faded/blurred scan    |        400–500 | OCR accuracy              |
| Very poor scan        |            500+ | Manual review recommended |

Higher DPI increases memory consumption and processing time.

For most documents, **300 DPI is the recommended starting point**.

## Output conventions

The generated document follows these conventions:

```markdown
# Document Title

## Table of Contents

* **Chapter I** ................................... Page 1
* **Section 1** ................................... Page 4
  * **Section 1(1)** .............................. Page 4

---

<!-- Original scanned page 4 -->

## Section 1 — Title

Text...

> Provided that...

### Schedule I

| Column 1 | Column 2 |
|---|---|
| Value | Value |
```

Running headers and footers are removed where confidently identified.

Original page boundaries remain identifiable through HTML comments.

## Accuracy policy

The application performs conservative OCR cleanup.

It should correct obvious artifacts such as:

```text
Rs. 50,000
```

to:

```text
₹50,000
```

when the context clearly identifies an Indian currency amount.

It should **not** silently rewrite ambiguous legal language.

Where OCR confidence is poor, manual verification against the source scan is required.

## Supported platforms

### Windows

Supported with:

* Python 3.12+
* Tesseract OCR
* PowerShell
* Git

### macOS

Supported with:

* Python 3.12+
* Homebrew
* Tesseract OCR

### Linux

Supported with:

* Python 3.12+
* Tesseract OCR
* system development packages

## Common problems

| Symptom                          | First action                                 |
| -------------------------------- | -------------------------------------------- |
| `tesseract is not recognized`  | Check Tesseract installation/PATH            |
| `ModuleNotFoundError`          | Activate`.venv` and reinstall requirements |
| OCR is poor                      | Increase DPI and improve preprocessing       |
| Tables are malformed             | Inspect table boundaries and source scan     |
| Windows script cannot run        | Check PowerShell execution policy            |
| CI fails but local build works   | Compare Python and dependency versions       |
| Output contains repeated headers | Review repeated-line detection               |
| ₹ appears incorrectly           | Verify UTF-8 output and font/editor support  |

Detailed runbooks are available in [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

## Development

Run the test suite:

```bash
python -m pytest
```

Run with verbose output:

```bash
python -m pytest -v
```

Check syntax:

```bash
python -m compileall src
```

## Contribution standards

Contributions should:

1. Preserve source-document accuracy.
2. Avoid destructive OCR corrections.
3. Include tests for processing changes.
4. Keep platform-specific behavior documented.
5. Avoid introducing dependencies without a clear reason.
6. Preserve UTF-8 compatibility.
7. Update documentation when CLI behavior changes.

Before submitting a change:

```bash
python -m pytest
python -m compileall src
```

For extraction changes, test against at least one scanned document and one text-based PDF.

## Maintainer

**Maintainer:** Phuchung

**Project:** PDF Markdown Cleaner

For project issues, use the repository's GitHub Issues tracker.

## License

This project is released under the MIT License.

See [LICENSE](LICENSE).

## Documentation

| Document                                     | Purpose                                     |
| -------------------------------------------- | ------------------------------------------- |
| [README.md](README.md)                        | Project overview and quickstart             |
| [SETUP.md](docs/SETUP.md)                     | Complete installation and development setup |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Diagnostics and failure runbooks            |

---

**Version:** 1.0.0
