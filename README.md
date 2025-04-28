# 📚 pdf-md-cleaner

> **Convert and clean** PDF, DOC, DOCX, and TXT files into **beautiful, clean Markdown**, while preserving folder structures and file naming.

<p align="center">
  <img src="https://img.shields.io/github/license/phuchungbhutia/pdf-md-cleaner?style=for-the-badge" />
  <img src="https://img.shields.io/github/issues/phuchungbhutia/pdf-md-cleaner?style=for-the-badge" />
  <img src="https://img.shields.io/github/stars/phuchungbhutia/pdf-md-cleaner?style=for-the-badge" />
  <img src="https://img.shields.io/github/forks/phuchungbhutia/pdf-md-cleaner?style=for-the-badge" />
  <img src="https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge" />
</p>

---

## ✨ Features

- 📄 **Convert**: `.pdf`, `.docx`, `.doc`, `.txt` ➔ `.md`
- 🧹 **Clean**: Remove headers, footers, page numbers, file titles
- 🧠 **Fix**: Broken paragraphs, text orientation, messy tables
- 📚 **Preserve**: Folder structure & filenames
- 🛠 **Docker support**: Easily run inside containers
- 🔥 **Pre-commit hooks**: Auto-format code before committing
- 🚀 **One Command**: `make run` to process all documents!

---

## 📂 Project Structure

```plaintext
pdf-md-cleaner/
├── cleaner/
│   ├── file_converter.py      # Converts supported formats to Markdown
│   ├── markdown_cleaner.py    # Cleans and formats Markdown
├── example/                   # Place your input files here
├── output/                    # Converted and cleaned Markdown files
├── tests/
│   └── test_cleaner.py         # Starter test cases
├── main.py                     # Main entry point
├── Dockerfile                  # For containerized usage
├── Makefile                    # For easy one-command operations
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
├── README.md                   # This file
├── CONTRIBUTING.md             # How to contribute
├── .gitignore                  # Ignore patterns
└── .pre-commit-config.yaml     # Pre-commit hooks
```

---

## 🚀 Quick Start

### 1. Clone the Repo

```bash
git clone https://github.com/phuchungbhutia/pdf-md-cleaner.git
cd pdf-md-cleaner
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
pre-commit install  # (Optional) for auto-formatting
```

### 3. Add Input Files

Place `.pdf`, `.docx`, `.doc`, or `.txt` files inside the `example/` folder.

### 4. Run the Script

```bash
python main.py
```

OR using Makefile:

```bash
make run
```

---

## 🛠 Tech Stack

- **Python 3.8+**
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF extraction
- [mammoth](https://github.com/mwilliamson/python-mammoth) — DOCX ➔ Markdown
- [markdownify](https://github.com/matthewwithanm/python-markdownify) — HTML ➔ Markdown
- **Black / Flake8** — Code formatting and linting
- **Docker** — Easy deployments

---

## 📦 Docker Support

Run everything inside a Docker container:

```bash
docker build -t pdf-md-cleaner .
docker run --rm -v "$PWD/example:/app/example" -v "$PWD/output:/app/output" pdf-md-cleaner
```

✅ No local installs needed.

---

## 🔍 How It Works

| Step | Action | Output Folder |
|:----:|:------:|:-------------:|
| 1 | Convert input files | `output/` |
| 2 | Clean Markdown | `output/` |

- **Conversion**: PDF/DOCX/DOC/TXT ➔ basic Markdown
- **Cleaning**: Remove repeated titles, fix paragraphs, clean tables

---

## 📈 GitHub Stats

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api/pin/?username=phuchungbhutia&repo=pdf-md-cleaner&theme=tokyonight" />
</p>

---

## 👥 Contributors

Thanks to all contributors ❤️

<a href="https://github.com/phuchungbhutia/pdf-md-cleaner/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=phuchungbhutia/pdf-md-cleaner" />
</a>

---

## 🧩 Future Plans

- [ ] Smarter table handling
- [ ] Dynamic heading detection
- [ ] CLI argument parser (input/output/custom rules)
- [ ] Deployable Docker image
- [ ] GitHub Actions for CI

---

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before contributing!  
We welcome all pull requests, suggestions, and improvements.

---

## 📜 License

Licensed under the [MIT License](LICENSE).

---
```

---

# 🔥 Summary of Enhancements:
- **Centered badges** at top.
- **Modern structure** and bulleting.
- **Docker usage instructions**.
- **Makefile usage instructions**.
- **Full GitHub stats**, contributors image.
- **Smoother sectioning** (with emojis and dividers).

---
