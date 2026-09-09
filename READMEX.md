# PDF Markdown Cleaner

[![CI](https://img.shields.io/github/actions/workflow/status/phuchungbhutia/pdf-md-cleaner/ci.yml?label=CI)](../../actions)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-1.0.0-informational)](../../releases)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#supported-platforms)

PDF Markdown Cleaner is an automated document-processing pipeline for converting scanned and text-based PDF documents into clean, structured, publication-ready Markdown.

It is purpose-built for legal and institutional records where standard PDF-to-text extractors fail, particularly **government audit manuals, statutory rules, legislation, registers, schedules, and annexures**.

The pipeline coordinates native PDF extraction, high-resolution rendering, adaptive image preprocessing, OCR with Tesseract, document structural reconstruction, table detection, OCR noise filtering, and Markdown formatting.

---

## What Problem Does It Solve?

Standard extractors dump layout fragments, margin speckles, and headers inline:

```text
Section 19 Audit of accounts
of local bodies shall be...
Page 23
GOVERNMENT OF SIKKIM
23
accounts
...

```

PDF Markdown Cleaner reconstructs semantic hierarchy, purges scanner noise, and generates clean Markdown:

```markdown
<!-- Source page 23 -->

## Section 19 — Audit of Accounts

The accounts of local bodies shall be audited in accordance with the provisions of this Act.

### Table of Contents

* [Section 19 — Audit of Accounts](#section-19--audit-of-accounts) *(page 23)*

```

---

## Core Capabilities

| Capability                                 | Description                                                                        |
| ------------------------------------------ | ---------------------------------------------------------------------------------- |
| **Batch Directory Processing**       | Converts every PDF found inside a folder (default:`input/`) in one pass.         |
| **Native & Scanned Handling**        | Automatically uses native text layers; falls back to OCR when text is sparse.      |
| **Windows Tesseract Auto-Discovery** | Detects default installation paths automatically without manual PATH setup.        |
| **Image Preprocessing**              | Edge noise stripping, Otsu binarization, and median blurring via OpenCV.           |
| **Structure Reconstruction**         | Recognizes Chapters, Rules, Annexures, and numbered legal clauses.                 |
| **Table Formatting**                 | Extracts tabular layouts into GitHub-flavored Markdown tables.                     |
| **Noise Filtering**                  | Strips scanning artifacts, border smudges, and isolated OCR hallucinations.        |
| **Page Traceability**                | Preserves original document page references with HTML source comments.             |
| **Audit Reporting**                  | Generates companion`.report.json` files with page-by-page OCR confidence scores. |

---

## Architecture

```text
                         ┌───────────────────┐
                         │   Input PDF(s)    │
                         │ (File / Directory)│
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   Text Detection  │
                         │      PyMuPDF      │
                         └─────────┬─────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │ Native Text                 │ Scanned Page
                    ▼                             ▼
       ┌───────────────────────┐     ┌───────────────────────┐
       │ Extraction & Clean-up │     │  OpenCV Preprocessing │
       └───────────┬───────────┘     └───────────┬───────────┘
                   │                             │
                   │                             ▼
                   │                 ┌───────────────────────┐
                   │                 │     Tesseract OCR     │
                   │                 └───────────┬───────────┘
                   │                             │
                   └──────────────┬──────────────┘
                                  ▼
                         ┌───────────────────┐
                         │ Structure Parser  │
                         │ (Chapters, Rules) │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Markdown / Tables │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │  output/*.md      │
                         │  output/*.json    │
                         └───────────────────┘

```

---

## Project Structure

```text
pdf-md-cleaner/
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .gitignore
│
├── src/
│   └── pdf_md_cleaner/
│       ├── __init__.py
│       ├── cli.py             # CLI parser and batch controller
│       ├── config.py          # CleanerConfig dataclass
│       ├── models.py          # PageResult and DocumentResult models
│       ├── ocr.py             # Tesseract wrapper & auto-path resolution
│       ├── preprocessing.py   # OpenCV binarization and margin cleaning
│       ├── extraction.py      # Dual native/OCR page extraction router
│       ├── pdf.py             # PyMuPDF rendering and native text utils
│       ├── tables.py          # Tabular detection and markdown tables
│       ├── structure.py       # Chapter, section, and rule hierarchy detection
│       ├── cleanup.py         # Noise elimination, hyphenation, regex cleanup
│       └── markdown.py        # Final Markdown compilation & TOC assembly
│
├── tests/
│   ├── test_cleanup.py
│   ├── test_markdown.py
│   ├── test_pipeline.py
│   └── test_structure.py
│
├── input/                     # Default location for input PDFs
│   └── source.pdf
│
├── output/                    # Generated Markdown and audit reports
│   └── source.md
│
└── docs/
    ├── SETUP.md
    └── TROUBLESHOOTING.md

```

---

## Quickstart

### 1. Prerequisites

* **Python 3.12+**
* **Tesseract OCR**:
* **Windows**: `winget install UB-Mannheim.TesseractOCR`
* **macOS**: `brew install tesseract`
* **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`

### 2. Setup Virtual Environment

**Windows (PowerShell):**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

```

**Linux / macOS:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```

---

## How to Run

Execute the package directly via Python's `-m` switch from the repository root:

### Batch Mode (Default)

Place your PDFs into the `input/` folder and run without arguments:

```powershell
python -m pdf_md_cleaner.cli

```

*Processes all `.pdf` files in `./input` and outputs `.md` and `.report.json` files to `./output`.*

### Single File Execution

```powershell
python -m pdf_md_cleaner.cli input/test.pdf -o output/test.md

```

### Custom Directories

```powershell
python -m pdf_md_cleaner.cli path/to/manuals/ -o converted_markdown/

```

### CLI Flags & Tuning

| Option               | Default      | Description                                  |
| -------------------- | ------------ | -------------------------------------------- |
| `input_path`       | `input/`   | Specific PDF file or directory of PDFs       |
| `-o`, `--output` | `output/`  | Destination Markdown file or directory       |
| `--dpi`            | `300`      | Rendering resolution for scanned pages       |
| `--language`       | `eng`      | Tesseract language code                      |
| `--no-toc`         | *Disabled* | Suppress automatic Table of Contents         |
| `--no-tables`      | *Disabled* | Disable rule-based table extraction          |
| `--report`         | *None*     | Explicit path for the JSON confidence report |

#### Higher DPI for Faint or Aged Scans:

```powershell
python -m pdf_md_cleaner.cli input/test.pdf -o output/test.md --dpi 400

```

---

## Testing & Quality Control

The project uses `pytest` and `ruff`. All PRs and pushes are verified against GitHub Actions.

```powershell
# Run the test suite
python -m pytest -v

# Run linter and formatting checks
ruff check src tests

# Apply automated fixes (e.g., trailing newlines)
ruff check --fix src tests

```

---

## Accuracy Policy

The cleaner follows conservative transformation rules:

1. **No Synthetic Text:** Never generates or guesses words that are unreadable in the scan; flags low-confidence sections with review markers.
2. **Indian Government Standards:** Standardizes common Indian official acronyms and terminology (e.g., `LBA (HQ)`, `ATIR`, `PRIs/ULBs`).
3. **Format Retention:** Reconstructs financial registers, pro-formas, and legal clauses into standard Markdown without flattening indentations.

---

## License

This project is released under the [MIT License](https://www.google.com/search?q=LICENSE).
