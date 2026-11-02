# One-time setup for the Prompt Improvement Lab.
# Creates the Python venv, installs backend + frontend dependencies, and
# makes sure backend\.env exists. Run this once; then use run.ps1.

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

Write-Host "== Backend ==" -ForegroundColor Cyan
Set-Location "$root\backend"
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created backend\.env - open it and paste your GEMINI_API_KEY" -ForegroundColor Yellow
}

Write-Host "== Frontend ==" -ForegroundColor Cyan
Set-Location "$root\frontend"
npm install

Set-Location $root
Write-Host ""
Write-Host "Setup complete. Make sure backend\.env has your GEMINI_API_KEY," -ForegroundColor Green
Write-Host "then start everything with:  .\run.ps1" -ForegroundColor Green
