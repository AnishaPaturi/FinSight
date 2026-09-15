# FinSight Launcher Script (PowerShell)
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "   FinSight - AI Stock Intelligence Platform     " -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Set environment
$env:PYTHONPATH = "."
$env:PYTHONIOENCODING = "utf-8"

Write-Host "Starting Unified FinSight Application on http://localhost:8000..." -ForegroundColor Green
Write-Host "Swagger API Docs available at http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop.`n"

.\venv\Scripts\python -m backend.main
