@echo off
echo =================================================
echo    FinSight - AI Stock Intelligence Platform     
echo =================================================
set PYTHONPATH=.
set PYTHONIOENCODING=utf-8

echo Starting Unified FinSight Application on http://localhost:8000...
echo Swagger API Docs available at http://localhost:8000/docs
echo.

.\venv\Scripts\python -m backend.main
pause
