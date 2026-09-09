param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,

    [Parameter(Mandatory=$true)]
    [string]$OutputFile
)

$ErrorActionPreference = "Stop"

if (-Not (Test-Path $InputFile)) {
    Write-Error "Input PDF not found: $InputFile"
    exit 1
}

if (-Not (Test-Path ".venv")) {
    Write-Error "Virtual environment not found. Run setup-windows.ps1 first."
    exit 1
}

& ".\.venv\Scripts\Activate.ps1"

python -m pdf_md_cleaner `
    "$InputFile" `
    --output "$OutputFile" `
    --dpi 300 `
    --lang eng `
    --min-confidence 70 `
    --report "$($OutputFile -replace '\.md$', '.report.json')"

if ($LASTEXITCODE -ne 0) {
    Write-Error "PDF processing failed."
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Finished."
Write-Host "Markdown: $OutputFile"