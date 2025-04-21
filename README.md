# 🧹 PDF Markdown Cleaner

Effortlessly clean and optimize Markdown files converted from PDFs — remove junk, fix formatting, and retain document structure.

![License](https://img.shields.io/github/license/phuchungbhutia/pdf-md-cleaner)
![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Build](https://img.shields.io/github/actions/workflow/status/phuchungbhutia/pdf-md-cleaner/python-app.yml)
![Issues](https://img.shields.io/github/issues/phuchungbhutia/pdf-md-cleaner)

## Features

✅ Remove repeated page headers, footers, and page numbers  
✅ Merge broken lines and fix paragraph flow  
✅ Auto-convert ALL CAPS to Markdown headings  
✅ Lightweight and customizable with regex  
✅ Easy to plug into your existing MD processing pipeline

## 🎬 Demo

> _Drop a before/after GIF here if you like. Use [Licecap](https://www.cockos.com/licecap/) or similar._
 
Before:	After:
Page 1	
THIS IS A HEADING	## This Is A Heading
Some text	Some text More text continues.
More text

## 🧰 Getting Started

### 📁 Project File Structure
```css
pdf-md-cleaner/
├── cleaner/
│   ├── __init__.py
│   └── markdown_cleaner.py
├── tests/
│   └── test_cleaner.py
├── example/
│   └── sample.md
├── .gitignore
├── README.md
├── requirements.txt
└── main.py
```

### 🔧 Usage

1. Put your `.md` file in the `example/` folder
2. Edit `main.py` to point to the right file
3. Run the script:

```bash
python main.py
```
4. Cleaned file will be saved as example/cleaned_sample.md


### 🧪 Run tests
```bash
pytest tests/
```

### 🛠️ Customize
Edit the regex patterns in main.py to fit your document.

### 🐍 Requirements

- Python 3.7+
- `pytest` for testing

### 📦 Install

```bash
git clone https://github.com/phuchungbhutia/pdf-md-cleaner.git
cd pdf-md-cleaner
pip install -r requirements.txt
```
---

### 📂 `.gitignore`

```gitignore
__pycache__/
*.pyc
.env
*.md~ 
*.log
.idea/
.vscode/
```

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
## 🗺️ Roadmap
 Core line cleaning and heading recognition

 Improved table structure parser

 CLI support with file input/output options

 Optional GUI using Tkinter or Textual

---
## 👥 Contributors
<a href="https://github.com/phuchungbhutia/pdf-md-cleaner/graphs/contributors"> <img src="https://contrib.rocks/image?repo=phuchungbhutia/pdf-md-cleaner" /> </a>
---

## 📊 GitHub Stats
<p align="center"> <img src="https://github-readme-stats.vercel.app/api/pin/?username=phuchungbhutia&repo=pdf-md-cleaner&theme=tokyonight" /> </p>
---

## 📜 License
This project is licensed under the MIT License. See LICENSE for more info.
---