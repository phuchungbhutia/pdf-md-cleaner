$ErrorActionPreference = "Stop"

if (-Not (Test-Path ".venv")) {
    Write-Error "Virtual environment not found."
    exit 1
}

& ".\.venv\Scripts\Activate.ps1"

$files = Get-ChildItem `
    -Path ".\input" `
    -Filter "*.pdf" `
    -File

if ($files.Count -eq 0) {
    Write-Host "No PDF files found in input folder."
    exit 0
}

foreach ($file in $files) {

    $outputName = [System.IO.Path]::GetFileNameWithoutExtension(
        $file.Name
    ) + ".md"

    $outputPath = Join-Path `
        ".\output" `
        $outputName

    Write-Host ""
    Write-Host "===================================="
    Write-Host "Processing: $($file.Name)"
    Write-Host "===================================="

    python -m pdf_md_cleaner `
        "$($file.FullName)" `
        --output "$outputPath" `
        --dpi 300 `
        --lang eng `
        --min-confidence 70
}

Write-Host ""
Write-Host "Batch processing complete."