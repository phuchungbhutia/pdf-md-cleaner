# 📚 pdf-md-cleaner

> **Convert and clean** PDF, DOC, DOCX, and TXT files into **beautiful, clean Markdown** — preserving folder structure and filenames.

![License](https://img.shields.io/github/license/phuchungbhutia/pdf-md-cleaner)
![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Build](https://img.shields.io/github/actions/workflow/status/phuchungbhutia/pdf-md-cleaner/python-app.yml)
![Issues](https://img.shields.io/github/issues/phuchungbhutia/pdf-md-cleaner)

<p align="center">
  <img src="https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge" />
</p>

---

## ✨ Features

- 📄 **Convert**: PDF, DOCX, DOC, TXT ➔ Markdown
- 🧹 **Clean**: Remove headers, footers, page numbers
- 🧠 **Fix**: Broken paragraphs, heading structures
- 🛠 **Preserve**: Original filenames and folder hierarchy
- 🚀 **Easy to use**: Run a single Python script to process everything!

---

## 📂 Project Structure

```plaintext
pdf-md-cleaner/
├── cleaner/
│   ├── file_converter.py      # Converts various formats to Markdown
│   ├── markdown_cleaner.py    # Cleans Markdown files
├── example/                   # Place your input files here
├── output/
│   ├── converted/              # Markdown after conversion
│   ├── cleaned/                # Final cleaned Markdown
├── tests/
│   └── test_cleaner.py
├── main.py                     # Main script
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/phuchungbhutia/pdf-md-cleaner.git
cd pdf-md-cleaner
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Add Your Files

Place `.pdf`, `.docx`, `.doc`, `.txt` files into the `example/` folder.

### 4. Run the Script

```bash
python main.py
```

### 5. Check Results

- Converted Markdown: `output/converted/`
- Cleaned Markdown: `output/cleaned/`

---

## ⚙️ How It Works

| Step | Action | Output Folder |
|:----:|:------:|:-------------:|
| 1 | Convert input files | `output/converted/` |
| 2 | Clean Markdown | `output/cleaned/` |

- **Conversion:** PDF, DOCX, DOC, TXT ➔ basic Markdown
- **Cleaning:** Remove headers, fix paragraphs, auto-create headings

---

## 🛠 Tech Stack

- Python 3.8+
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) — PDF extraction
- [python-docx](https://python-docx.readthedocs.io/en/latest/) — DOCX parsing
- [markdownify](https://pypi.org/project/markdownify/) — HTML ➔ Markdown
- Regex — Pattern matching and cleaning

---

## 🚧 Future Improvements

- [ ] Auto-detect and fix complex tables
- [ ] Advanced heading hierarchy based on font size
- [ ] CLI Interface (choose file/folder/cleaning rules via terminal)
- [ ] Docker container for easy deployment
- [ ] GitHub Action for automatic processing

---


# 🎯 One Liner

> **pdf-md-cleaner**: Turn your messy documents into clean, structured Markdown — effortlessly!

---

### 📦 Install

```bash
git clone https://github.com/phuchungbhutia/pdf-md-cleaner.git
cd pdf-md-cleaner
pip install -r requirements.txt
```
---


### 🌐 GitHub Setup Tips
```bash
# Initialize and push to GitHub
git init
git add .
git commit -m "Initial commit"
gh repo create pdf-md-cleaner --public --source=. --remote=origin --push
```
or
### You already created a GitHub repo manually
If you've already created a repo at https://github.com/phuchungbhutia/pdf-md-cleaner, just run:

```bash
git remote add origin https://github.com/phuchungbhutia/pdf-md-cleaner.git
git branch -M main
git push -u origin main
```
or 
### Update
```bash
git add .
git commit -m "Update"
git push
```
---
## 👥 Contributors
<a href="https://github.com/phuchungbhutia/pdf-md-cleaner/graphs/contributors"> <img src="https://contrib.rocks/image?repo=phuchungbhutia/pdf-md-cleaner" /> </a>

---

## 📊 GitHub Stats
<p align="center"> <img src="https://github-readme-stats.vercel.app/api/pin/?username=phuchungbhutia&repo=pdf-md-cleaner&theme=tokyonight" /> </p>

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api/pin/?username=phuchungbhutia&repo=pdf-md-cleaner&theme=radical" />
</p>

---

## 📜 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for more info.
