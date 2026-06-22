@echo off
chcp 65001 >nul 2>&1
title Callie Social Content Tool v2

echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo [2/3] Setting up virtual environment...
if not exist "venv" (
    echo Creating venv...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo Dependencies installed

echo [3/3] Starting server on port 8000...
echo Open http://localhost:8000 in your browser
echo Press Ctrl+C to stop server
echo.

python -m uvicorn app:app --host 127.0.0.1 --port 8000

pause