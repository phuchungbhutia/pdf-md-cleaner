$ErrorActionPreference = "Stop"

Write-Host "===================================="
Write-Host " PDF Markdown Cleaner Setup"
Write-Host "===================================="
Write-Host ""

Write-Host "Checking Python..."

python --version

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Python 3.12 was not found."
    Write-Host "Install Python 3.12 and try again."
    exit 1
}

Write-Host ""
Write-Host "Creating virtual environment..."

if (-Not (Test-Path ".venv")) {
    python -m venv .venv
}

Write-Host ""
Write-Host "Activating virtual environment..."

& ".\.venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Upgrading pip..."

python -m pip install --upgrade pip setuptools wheel

Write-Host ""
Write-Host "Installing project dependencies..."

python -m pip install -r requirements.txt

Write-Host ""
Write-Host "Installing project in editable mode..."

python -m pip install -e .

Write-Host ""
Write-Host "Checking dependencies..."

python -m pip check

Write-Host ""
Write-Host "Running tests..."

python -m pytest -v

Write-Host ""
Write-Host "Running Ruff..."

ruff check src tests

Write-Host ""
Write-Host "===================================="
Write-Host " Setup complete"
Write-Host "===================================="