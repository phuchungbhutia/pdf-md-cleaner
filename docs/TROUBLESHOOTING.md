# PDF Markdown Cleaner — Troubleshooting Guide

This guide provides operational runbooks for installation, OCR, PDF extraction, Markdown generation, and CI failures.

Return to the [project README](../README.md).

## 1. Triage checklist

Run the following commands before changing anything.

### Linux/macOS

```bash
python --version
which python
python -m pip --version
tesseract --version
which tesseract
pip check
git status
```

### Windows PowerShell

```powershell
python --version
Get-Command python
python -m pip --version
tesseract --version
Get-Command tesseract
pip check
git status
```

Then verify imports:

```bash
python -c "import fitz, pdfplumber, cv2, pytesseract; print('Imports OK')"
```

Verify the PDF exists:

```bash
ls -lh input/
```

Windows:

```powershell
Get-ChildItem input
```

Verify output:

```bash
ls -lh output/
```

Windows:

```powershell
Get-ChildItem output
```

# 2. Python is not found

## Issue Summary

The command:

```text
python
```

returns an error such as:

```text
python: command not found
```

or:

```text
'python' is not recognized as an internal or external command
```

## Root Cause Analysis

Python is either not installed or its executable is not available through PATH.

## Exact Resolution Steps

Windows:

```powershell
py --version
```

If this works:

```powershell
py -3.12 -m venv .venv
```

macOS/Linux:

```bash
python3.12 --version
```

If Python is missing, install Python 3.12 and repeat the verification.

## Verification Command

```bash
python --version
```

Expected:

```text
Python 3.12.x
```

# 3. Virtual environment is not active

## Issue Summary

Packages appear installed, but:

```bash
python -c "import fitz"
```

fails.

## Root Cause Analysis

The shell is using a different Python installation.

## Exact Resolution Steps

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then:

```bash
python -m pip install -r requirements.txt
```

## Verification Command

Linux/macOS:

```bash
which python
```

Windows:

```powershell
Get-Command python
```

The path should point inside `.venv`.

# 4. `ModuleNotFoundError`

## Issue Summary

The application reports:

```text
ModuleNotFoundError: No module named 'fitz'
```

or another missing package.

## Root Cause Analysis

The dependency was not installed into the active Python environment.

## Exact Resolution Steps

Activate `.venv` and run:

```bash
python -m pip install -r requirements.txt
```

Do not rely on a global `pip` executable.

Use:

```bash
python -m pip
```

instead.

## Verification Command

```bash
python -c "import fitz, pdfplumber, cv2, pytesseract; print('Dependencies OK')"
```

# 5. Tesseract is not recognized

## Issue Summary

The program fails because Tesseract cannot be found.

Typical Windows error:

```text
tesseract is not recognized
```

Typical Linux/macOS error:

```text
TesseractNotFoundError
```

## Root Cause Analysis

Tesseract is not installed or its executable is not in PATH.

## Exact Resolution Steps

Windows:

```powershell
Get-Command tesseract
```

If not found, add the Tesseract installation directory to PATH.

Typical location:

```text
C:\Program Files\Tesseract-OCR
```

Temporary PowerShell fix:

```powershell
$env:Path += ";C:\Program Files\Tesseract-OCR"
```

Linux:

```bash
sudo apt install tesseract-ocr
```

macOS:

```bash
brew install tesseract
```

## Verification Command

```bash
tesseract --version
```

# 6. Tesseract language data is missing

## Issue Summary

OCR fails with a message similar to:

```text
Error opening data file
```

## Root Cause Analysis

The requested Tesseract language package is not installed.

## Exact Resolution Steps

Check installed languages:

```bash
tesseract --list-langs
```

For English, the output should contain:

```text
eng
```

Run using:

```bash
--lang eng
```

If a language is absent, install its Tesseract language data for the operating system.

## Verification Command

```bash
tesseract --list-langs
```

# 7. OCR output is poor

## Issue Summary

The Markdown is generated but contains:

```text
broken words
wrong characters
missing punctuation
incorrect numbers
```

## Root Cause Analysis

Common causes include:

* Low-resolution source scans.
* Skewed pages.
* Faded text.
* Background noise.
* Stamps or handwriting over printed text.
* Multi-column layouts.
* Poor contrast.
* Complex tables.

## Exact Resolution Steps

Start at 300 DPI:

```bash
python legal_pdf_to_markdown.py \
    input/source.pdf \
    -o output/document.md \
    --dpi 300
```

If necessary:

```bash
python legal_pdf_to_markdown.py \
    input/source.pdf \
    -o output/document.md \
    --dpi 400
```

For extremely poor scans:

```bash
python legal_pdf_to_markdown.py \
    input/source.pdf \
    -o output/document.md \
    --dpi 500
```

## Verification Command

Compare several representative pages directly against the source PDF.

Do not validate OCR quality from only the first page.

# 8. OCR changes legal wording

## Issue Summary

A provision appears different from the scanned source.

## Root Cause Analysis

OCR can confuse visually similar characters:

```text
0 / O
1 / l / I
rn / m
cl / d
```

It can also merge or split words.

## Exact Resolution Steps

Open the original scanned page and compare the affected passage.

Do not automatically apply aggressive dictionary substitutions.

For legally significant text, manually verify:

* Section numbers.
* Rule numbers.
* Dates.
* Amounts.
* Percentages.
* Names.
* Government orders.
* References.
* Sub-rule numbering.
* Provisos.
* Exceptions.

## Verification Command

Search the generated Markdown for the affected provision:

```bash
grep -n "Section 19" output/document.md
```

Windows:

```powershell
Select-String "Section 19" output\document.md
```

# 9. Rupee symbol appears incorrectly

## Issue Summary

The output contains:

```text
Rs.
INR
?
â‚¹
```

instead of:

```text
₹
```

## Root Cause Analysis

The most common causes are:

* Incorrect source encoding.
* Non-UTF-8 editor.
* OCR artifact.
* Incorrect terminal encoding.

## Exact Resolution Steps

Ensure the Markdown file is written as UTF-8.

Python should explicitly use:

```python
Path("output.md").write_text(
    markdown,
    encoding="utf-8"
)
```

On Windows PowerShell, inspect the file using an editor with UTF-8 support.

## Verification Command

```bash
python -c "print('₹50,000/-')"
```

# 10. Tables are malformed

## Issue Summary

A source table becomes:

```text
Name Address Amount Date
John Gangtok 50000 2026
```

instead of a Markdown table.

## Root Cause Analysis

PDF tables are not necessarily stored as tables internally.

They may consist of:

* Independent text objects.
* Drawing lines.
* Images.
* Scanned text.
* Merged cells.
* Multi-page tables.

## Exact Resolution Steps

Confirm that `pdfplumber` can detect the table.

Test extraction independently:

```bash
python -c "import pdfplumber; p=pdfplumber.open('input/source.pdf'); print(p.pages[0].extract_tables())"
```

If the PDF is image-only, native table extraction may fail.

In that case, table-specific OCR/layout processing is required.

## Verification Command

Inspect generated Markdown for:

```markdown
| Column | Column |
|---|---|
```

Every Markdown table should have a header separator row.

# 11. Multi-column pages are incorrectly ordered

## Issue Summary

Text appears in the wrong reading order.

Example:

```text
Left column paragraph A
Right column paragraph B
Left column paragraph C
Right column paragraph D
```

becomes:

```text
A B C D
```

or another incorrect order.

## Root Cause Analysis

OCR engines may interpret the page as a single text region.

## Exact Resolution Steps

Identify the affected page.

Render it separately at high resolution.

Compare the OCR ordering against the original page.

For production-grade multi-column support, process the page as separate layout regions before OCR.

## Verification Command

Inspect the generated page-specific section:

```bash
grep -n "Original scanned page 23" output/document.md
```

# 12. Repeated headers remain

## Issue Summary

Every page contains:

```text
GOVERNMENT OF SIKKIM
LOCAL FUND AUDIT MANUAL
```

and the lines remain in the body.

## Root Cause Analysis

The repeated-header detector may not have recognized the line because OCR changed it slightly on different pages.

## Exact Resolution Steps

Normalize OCR output before comparison.

For known documents, maintain a document-specific list of headers where necessary.

Avoid deleting short lines globally because they may be legitimate legal headings.

## Verification Command

```bash
grep -n "GOVERNMENT OF SIKKIM" output/document.md
```

# 13. Page numbers remain in body text

## Issue Summary

The output contains standalone:

```text
23
24
25
```

between paragraphs.

## Root Cause Analysis

Page numbers are extracted as ordinary text.

## Exact Resolution Steps

Use conservative page-number detection.

Do not remove all numeric lines because legal documents legitimately contain:

```text
19.
(1)
2026
₹50,000
```

Only remove lines matching known page-number patterns.

## Verification Command

Search suspicious standalone numbers:

```bash
grep -nE '^[0-9]+$' output/document.md
```

Review results before deleting anything manually.

# 14. Form fields are damaged

## Issue Summary

A statutory form contains lines such as:

```text
Name..............
Address___________
Date-------------
```

## Root Cause Analysis

OCR interprets visual form lines as punctuation or random characters.

## Exact Resolution Steps

Normalize field lines to:

```text
Name: ____________________
Address: ____________________
Date: ____________________
```

For complex forms, use Markdown tables:

```markdown
| Field | Entry |
|---|---|
| Name | ____________________ |
| Address | ____________________ |
| Date | ____________________ |
```

## Verification Command

Search:

```bash
grep -n "____________________" output/document.md
```

# 15. Markdown heading hierarchy is incorrect

## Issue Summary

The output contains:

```markdown
## Rule 1
## (1)
## (2)
```

instead of a hierarchy such as:

```markdown
## Rule 1

### (1)

### (2)
```

## Root Cause Analysis

Heading detection is pattern-based and cannot always determine the legal hierarchy from typography alone.

## Exact Resolution Steps

Review:

* Chapter headings.
* Part headings.
* Section headings.
* Rule headings.
* Sub-rules.
* Clauses.
* Sub-clauses.
* Schedules.
* Forms.

Do not promote ordinary legal paragraphs to Markdown headings merely because they begin with numbers.

## Verification Command

```bash
grep -n '^#' output/document.md
```

# 16. Table of Contents is incomplete

## Issue Summary

Some sections or schedules do not appear in the generated TOC.

## Root Cause Analysis

The heading detector failed to recognize a heading because of:

* OCR corruption.
* Unusual typography.
* Missing section number.
* Multi-line heading.
* Decorative text.
* Scanned image quality.

## Exact Resolution Steps

Search for the missing heading:

```bash
grep -n "Schedule" output/document.md
```

Windows:

```powershell
Select-String "Schedule" output\document.md
```

Add or improve the relevant heading detection rule.

Then regenerate the document.

## Verification Command

Compare the TOC against the source document's:

* Contents page.
* Chapters.
* Sections.
* Rules.
* Schedules.
* Forms.
* Annexures.

# 17. Output file is empty

## Issue Summary

The generated Markdown exists but contains little or no text.

## Root Cause Analysis

Possible causes:

1. OCR returned no text.
2. PDF pages are blank.
3. Tesseract failed.
4. Image preprocessing destroyed the text.
5. The wrong PDF was supplied.

## Exact Resolution Steps

Test Tesseract directly on a rendered page.

Confirm the OCR language:

```bash
tesseract --list-langs
```

Try a higher DPI.

If preprocessing produces a blank image, compare the processed image with the original.

## Verification Command

Check file size:

```bash
ls -lh output/document.md
```

Then:

```bash
wc -l output/document.md
```

# 18. Processing is extremely slow

## Issue Summary

A large PDF takes a very long time to process.

## Root Cause Analysis

The dominant costs are:

* High DPI rendering.
* Large page dimensions.
* OCR.
* Table extraction.
* Image preprocessing.

## Exact Resolution Steps

Start with:

```bash
--dpi 300
```

Avoid 600 DPI unless the source requires it.

Process a representative subset first when testing configuration.

Use an SSD for temporary page images.

## Verification Command

Monitor output:

```bash
time python legal_pdf_to_markdown.py input/source.pdf \
    -o output/document.md
```

# 19. System runs out of memory

## Issue Summary

The process terminates unexpectedly or the operating system reports insufficient memory.

## Root Cause Analysis

Rendering hundreds of pages at high resolution can consume substantial memory and disk space.

## Exact Resolution Steps

Reduce DPI:

```bash
--dpi 300
```

Process pages incrementally rather than keeping all images in memory.

Clean temporary files:

```bash
rm -rf work/pages/*
```

Windows:

```powershell
Remove-Item -Recurse -Force work\pages\*
```

## Verification Command

Check available storage and memory before processing large documents.

# 20. Windows path errors

## Issue Summary

The application reports errors such as:

```text
FileNotFoundError
```

despite the file appearing to exist.

## Root Cause Analysis

Common causes include:

```text
C:\new\test.pdf
```

where `\n` or other escape sequences become meaningful inside Python string literals.

## Exact Resolution Steps

Use `pathlib`:

```python
from pathlib import Path

pdf = Path(r"C:\new\test.pdf")
```

Or use forward slashes:

```python
pdf = Path("C:/new/test.pdf")
```

From PowerShell, use:

```powershell
python legal_pdf_to_markdown.py "C:\Documents\source.pdf" -o "output\document.md"
```

## Verification Command

```powershell
Test-Path "C:\Documents\source.pdf"
```

# 21. Encoding problems on Windows

## Issue Summary

Characters such as:

```text
₹
©
“
”
```

appear corrupted.

## Root Cause Analysis

The source, terminal, editor or generated file may use incompatible encodings.

## Exact Resolution Steps

Ensure Python writes UTF-8:

```python
encoding="utf-8"
```

Use a UTF-8-capable editor.

For command-line inspection:

```powershell
Get-Content output\document.md -Encoding UTF8
```

## Verification Command

```powershell
python -c "print('UTF-8 test: ₹ © “text”')"
```

# 22. Git shows every line as changed

## Issue Summary

A small edit appears to modify an entire Markdown or Python file.

## Root Cause Analysis

Line endings changed between:

```text
CRLF
```

and:

```text
LF
```

## Exact Resolution Steps

Configure Git:

Windows:

```powershell
git config --global core.autocrlf true
```

Linux/macOS:

```bash
git config --global core.autocrlf input
```

Prefer a repository `.gitattributes` file:

```text
* text=auto
*.py text eol=lf
*.md text eol=lf
```

## Verification Command

```bash
git diff --ignore-space-at-eol
```

# 23. CI fails while local tests pass

## Issue Summary

GitHub Actions fails even though:

```bash
python -m pytest
```

passes locally.

## Root Cause Analysis

Common differences include:

* Python version.
* Dependency versions.
* Missing Tesseract.
* Operating system.
* Environment variables.
* File paths.
* Case-sensitive filesystem.
* Missing test fixtures.

## Exact Resolution Steps

Confirm CI uses the intended Python version.

Pin critical dependencies.

Install Tesseract in CI if OCR tests require it.

Avoid Windows-only paths.

Use:

```python
pathlib.Path
```

instead of hard-coded separators.

## Verification Command

Run the same Python version locally:

```bash
python --version
```

and compare with the CI configuration.

# 24. GitHub Actions cannot find Tesseract

## Issue Summary

CI reports:

```text
TesseractNotFoundError
```

## Root Cause Analysis

The CI runner does not automatically have the required OCR executable configured.

## Exact Resolution Steps

Install Tesseract in the workflow before running OCR tests.

For Ubuntu-based GitHub Actions:

```yaml
- name: Install Tesseract
  run: |
    sudo apt-get update
    sudo apt-get install -y tesseract-ocr
```

Then:

```yaml
- name: Verify Tesseract
  run: tesseract --version
```

## Verification Command

```bash
tesseract --version
```

# 25. Dependency versions changed unexpectedly

## Issue Summary

The same PDF produces different output after a dependency update.

## Root Cause Analysis

PDF and OCR libraries can change parsing or rendering behavior between releases.

## Exact Resolution Steps

Record dependencies:

```bash
pip freeze > requirements-lock.txt
```

Compare environments:

```bash
pip freeze
```

Use pinned versions for production workflows.

Run regression tests against representative PDFs after dependency upgrades.

## Verification Command

```bash
pip check
```

# 26. Cache causes stale output

## Issue Summary

The generated Markdown appears unchanged after modifying the code.

## Root Cause Analysis

The application may be reusing previously rendered pages or generated files.

## Exact Resolution Steps

Delete temporary output:

Linux/macOS:

```bash
rm -rf work output
mkdir -p work/pages output
```

Windows:

```powershell
Remove-Item -Recurse -Force work,output
New-Item -ItemType Directory -Force work,pages,output
```

Run the conversion again.

## Verification Command

Check the output timestamp:

```bash
ls -lh output/document.md
```

# 27. GitHub Pages or documentation links fail

## Issue Summary

Links work locally but fail on GitHub.

## Root Cause Analysis

Common causes:

* Absolute local paths.
* Windows backslashes.
* Incorrect capitalization.
* Incorrect relative path.
* File renamed without updating links.

## Exact Resolution Steps

Use GitHub-compatible relative links:

```markdown
[Setup Guide](docs/SETUP.md)
```

not:

```markdown
C:\project\docs\SETUP.md
```

Use forward slashes:

```markdown
[Setup](docs/SETUP.md)
```

## Verification Command

Inspect:

```bash
grep -R "C:\\\\" README.md docs/
```

and:

```bash
grep -R "\.\./" README.md docs/
```

Review every documentation link before publishing.

# 28. Legal-document validation checklist

Before publishing a transcription, verify:

```text
[ ] Original PDF preserved
[ ] Number of pages recorded
[ ] TOC checked
[ ] Chapters checked
[ ] Sections checked
[ ] Rules checked
[ ] Sub-rules checked
[ ] Provisos checked
[ ] Explanations checked
[ ] Schedules checked
[ ] Annexures checked
[ ] Forms checked
[ ] Registers checked
[ ] Tables checked
[ ] Dates checked
[ ] Monetary amounts checked
[ ] Section numbers checked
[ ] Government order references checked
[ ] Signature lines checked
[ ] Page references checked
[ ] OCR anomalies reviewed
[ ] UTF-8 verified
[ ] Markdown rendering checked
```

# 29. Recommended forensic comparison

For legally significant documents, perform a page-by-page comparison.

Use the original PDF as the authoritative source.

For each page:

```text
Source page
     ↓
OCR text
     ↓
Markdown text
     ↓
Manual comparison
     ↓
Correction
     ↓
Final verification
```

Pay particular attention to:

```text
₹ amounts
%
dates
decimal numbers
section numbers
rule numbers
sub-rule numbers
names
addresses
notifications
Government Orders
legal references
```

A single OCR character can change the meaning of a statutory provision.

# 30. Emergency clean rebuild

If the environment is suspected to be corrupted:

Linux/macOS:

```bash
deactivate 2>/dev/null || true
rm -rf .venv work output
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip check
python -m pytest
```

Windows:

```powershell
deactivate
Remove-Item -Recurse -Force .venv,work,output -ErrorAction SilentlyContinue
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip check
python -m pytest
```

Then verify OCR:

```bash
tesseract --version
```

Finally process a known-good test PDF.

# 31. Diagnostic bundle

When reporting an issue, collect:

```bash
python --version
python -m pip --version
pip check
tesseract --version
python -c "import fitz; print(fitz.__doc__)"
git status
```

Also record:

```text
Operating system:
Python version:
Tesseract version:
PDF page count:
PDF source type:
OCR language:
DPI:
Failure message:
Affected page:
Expected output:
Actual output:
```

Do not attach confidential or personally identifiable documents to public issue trackers.

# 32. Escalation rule

If an error cannot be reproduced with a small sample PDF, isolate the problem first.

Use:

```text
Full PDF
   ↓
Identify failing page
   ↓
Extract failing page
   ↓
Reproduce with one page
   ↓
Determine OCR/layout/table issue
   ↓
Fix component
   ↓
Run full document
```

This is substantially faster than repeatedly processing a large document while debugging a single damaged page.

---

## Related documentation

* [Project README](../README.md)
* [Setup Guide](SETUP.md)

## Maintainer

**PDF Markdown Cleaner**

Maintained by **Phuchung**.

The project should be treated as a document-processing and archival utility. Generated OCR output must be independently verified before being relied upon as an authoritative legal text.
