# Starts the backend and frontend together, each in its own window,
# then opens the app in your browser.

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

if (-not (Test-Path "$root\backend\.venv")) {
    Write-Host "Dependencies aren't installed yet. Run .\setup.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host "Starting backend on http://localhost:8000 ..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command",
    "cd '$root\backend'; & '.\.venv\Scripts\python.exe' app.py"

Write-Host "Starting frontend on http://localhost:5173 ..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command",
    "cd '$root\frontend'; npm run dev"

Start-Sleep -Seconds 4
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "Both servers are starting in their own windows." -ForegroundColor Green
Write-Host "  Frontend: http://localhost:5173  (open this)"
Write-Host "  Backend:  http://localhost:8000  (the API)"
Write-Host "Close those two windows to stop the servers."
