# PDF Markdown Cleaner — Setup Guide

This document describes the complete setup required to develop and run PDF Markdown Cleaner on Windows, macOS, and Linux.

Return to the [project README](../README.md).

## 1. System requirements

### Minimum

| Component        | Requirement                            |
| ---------------- | -------------------------------------- |
| Python           | 3.12 or later                          |
| RAM              | 4 GB                                   |
| Storage          | 2 GB free                              |
| Tesseract        | 5.x recommended                        |
| Operating system | Windows 10/11, macOS 13+, modern Linux |
| PDF input        | PDF 1.4+ recommended                   |

### Recommended

For large scanned legal documents:

| Component | Recommendation |
| --------- | -------------- |
| RAM       | 8–16 GB       |
| CPU       | 4+ cores       |
| Storage   | 10+ GB free    |
| OCR DPI   | 300–400       |
| Python    | 3.12+          |
| SSD       | Recommended    |

OCR is CPU-intensive. Large PDFs can also generate substantial temporary image data.

# 2. Windows setup

## 2.1 Install Python

Install Python 3.12 or newer.

Verify:

```powershell
py --version
```

Expected:

```text
Python 3.12.x
```

Also verify:

```powershell
python --version
```

If `python` is not available but `py` works, use `py -3.12`.

## 2.2 Install Git

Verify:

```powershell
git --version
```

## 2.3 Install Tesseract OCR

Install Tesseract OCR for Windows.

After installation, verify:

```powershell
tesseract --version
```

If PowerShell reports:

```text
tesseract : The term 'tesseract' is not recognized
```

locate the executable and add its installation directory to PATH.

A common installation directory is:

```text
C:\Program Files\Tesseract-OCR
```

For the current PowerShell session:

```powershell
$env:Path += ";C:\Program Files\Tesseract-OCR"
```

Verify:

```powershell
tesseract --version
```

For a permanent PATH configuration, use Windows Environment Variables and add:

```text
C:\Program Files\Tesseract-OCR
```

## 2.4 Create a virtual environment

From the repository root:

```powershell
py -3.12 -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 2.5 Upgrade pip

```powershell
python -m pip install --upgrade pip setuptools wheel
```

## 2.6 Install dependencies

```powershell
pip install -r requirements.txt
```

Verify:

```powershell
pip check
```

# 3. macOS setup

## 3.1 Install Homebrew

Verify:

```bash
brew --version
```

## 3.2 Install Tesseract

```bash
brew install tesseract
```

Verify:

```bash
tesseract --version
```

## 3.3 Install Python

```bash
brew install python@3.12
```

Verify:

```bash
python3.12 --version
```

## 3.4 Create the virtual environment

```bash
python3.12 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip setuptools wheel
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Verify:

```bash
pip check
```

# 4. Linux setup

## 4.1 Ubuntu/Debian

Update package information:

```bash
sudo apt update
```

Install Python and required system packages:

```bash
sudo apt install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0
```

Verify:

```bash
python3.12 --version
tesseract --version
```

## 4.2 Create the environment

```bash
python3.12 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Upgrade packaging tools:

```bash
python -m pip install --upgrade pip setuptools wheel
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

Verify:

```bash
pip check
```

# 5. Repository setup

Clone the repository:

```bash
git clone <repository-url>
cd pdf-md-cleaner
```

Check the repository:

```bash
git status
```

Expected:

```text
On branch main
nothing to commit, working tree clean
```

# 6. Recommended directory layout

Create working directories:

Linux/macOS:

```bash
mkdir -p input output work/pages
```

Windows:

```powershell
New-Item -ItemType Directory -Force input,output,work,pages
```

Recommended layout:

```text
pdf-md-cleaner/
├── input/
│   └── source.pdf
├── output/
│   └── document.md
├── work/
│   └── pages/
└── src/
```

Keep original PDFs in `input/`.

Generated files belong in `output/`.

Temporary OCR images belong in `work/`.

# 7. Environment configuration

The application does not require secrets for ordinary local OCR processing.

If a future deployment adds external OCR, storage, API or cloud processing, environment variables should be stored outside source control.

Example:

```text
.env
```

Example configuration:

```dotenv
PDF_MDC_DPI=300
PDF_MDC_LANGUAGE=eng
PDF_MDC_OUTPUT_ENCODING=utf-8
PDF_MDC_KEEP_IMAGES=false
```

Never commit credentials:

```gitignore
.env
.env.*
!.env.example
```

A safe template is:

```dotenv
PDF_MDC_DPI=300
PDF_MDC_LANGUAGE=eng
PDF_MDC_OUTPUT_ENCODING=utf-8
```

# 8. Dependency verification

List installed packages:

```bash
pip list
```

Check dependencies:

```bash
pip check
```

Test imports:

```bash
python -c "import fitz, pdfplumber, cv2, pytesseract; print('Dependencies OK')"
```

Test Tesseract:

```bash
tesseract --version
```

# 9. First document conversion

Place a PDF at:

```text
input/source.pdf
```

Run:

```bash
python legal_pdf_to_markdown.py \
    input/source.pdf \
    -o output/document.md
```

Windows PowerShell:

```powershell
python legal_pdf_to_markdown.py `
    input\source.pdf `
    -o output\document.md
```

# 10. High-quality OCR

For ordinary scans:

```bash
python legal_pdf_to_markdown.py \
    input/source.pdf \
    -o output/document.md \
    --dpi 300
```

For poor scans:

```bash
python legal_pdf_to_markdown.py \
    input/source.pdf \
    -o output/document.md \
    --dpi 400
```

For very difficult documents:

```bash
python legal_pdf_to_markdown.py \
    input/source.pdf \
    -o output/document.md \
    --dpi 500
```

Start at 300 DPI. Increase only when necessary.

# 11. Language configuration

English:

```bash
python legal_pdf_to_markdown.py input/source.pdf \
    -o output/document.md \
    --lang eng
```

Check installed Tesseract languages:

```bash
tesseract --list-langs
```

If additional language packs are installed, pass the appropriate language code.

Example:

```bash
--lang eng+hin
```

# 12. Build verification

Compile the Python source:

```bash
python -m compileall .
```

Run tests:

```bash
python -m pytest
```

Run verbose tests:

```bash
python -m pytest -v
```

Run a focused test:

```bash
python -m pytest tests/test_ocr.py -v
```

Check package integrity:

```bash
pip check
```

# 13. Output verification

After processing:

```bash
ls -lh output/
```

Windows:

```powershell
Get-ChildItem output
```

Check Markdown:

```bash
head -n 40 output/document.md
```

Windows:

```powershell
Get-Content output\document.md -TotalCount 40
```

Confirm the output contains:

```markdown
## Table of Contents
```

and original page markers such as:

```html
<!-- Original scanned page 1 -->
```

# 14. Daily workflow

| Task                 | Linux/macOS                                                    | Windows PowerShell                                             |
| -------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| Activate environment | `source .venv/bin/activate`                                  | `.\.venv\Scripts\Activate.ps1`                               |
| Install dependencies | `pip install -r requirements.txt`                            | `pip install -r requirements.txt`                            |
| Run tests            | `python -m pytest`                                           | `python -m pytest`                                           |
| Compile              | `python -m compileall .`                                     | `python -m compileall .`                                     |
| Check packages       | `pip check`                                                  | `pip check`                                                  |
| OCR PDF              | `python legal_pdf_to_markdown.py input/a.pdf -o output/a.md` | `python legal_pdf_to_markdown.py input\a.pdf -o output\a.md` |
| Git status           | `git status`                                                 | `git status`                                                 |
| Update code          | `git pull`                                                   | `git pull`                                                   |
| Create branch        | `git switch -c feature/name`                                 | `git switch -c feature/name`                                 |

# 15. Reproducible environment

Before committing dependency changes:

```bash
pip freeze > requirements-lock.txt
```

Review the generated file before committing it.

Do not blindly upgrade every package in a production OCR environment. OCR and PDF libraries can change extraction behavior between releases.

# 16. Git workflow

Create a feature branch:

```bash
git switch -c feature/improve-table-extraction
```

Run tests:

```bash
python -m pytest
```

Review changes:

```bash
git diff
```

Check status:

```bash
git status
```

Commit:

```bash
git add .
git commit -m "Improve table extraction"
```

Push:

```bash
git push -u origin feature/improve-table-extraction
```

# 17. Production document workflow

For important legal documents:

```text
1. Preserve original PDF
2. Calculate/check source checksum
3. Run extraction
4. Preserve generated Markdown
5. Review TOC
6. Review every table
7. Compare legal provisions with source
8. Review schedules and forms
9. Review signatures and declarations
10. Validate Markdown
11. Archive source + generated output
```

Never overwrite the original source PDF with a processed artifact.

# 18. Troubleshooting

When setup fails, begin with:

```bash
python --version
tesseract --version
pip --version
pip check
```

Then consult [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

# 19. Clean rebuild

Linux/macOS:

```bash
rm -rf .venv work output
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p work/pages output
```

Windows:

```powershell
Remove-Item -Recurse -Force .venv,work,output
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
New-Item -ItemType Directory -Force work,pages,output
```

A clean rebuild is useful when dependency state or generated OCR artifacts have become inconsistent.
