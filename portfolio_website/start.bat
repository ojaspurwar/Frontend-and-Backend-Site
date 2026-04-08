@echo off
REM FastAPI Portfolio Website - Quick Start

echo.
echo ========================================
echo FastAPI Portfolio Website Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install -r requirements.txt

echo [4/5] Creating database...
REM Database will be created automatically on first run

echo [5/5] Starting server...
echo.
echo ========================================
echo Server is running!
echo ========================================
echo.
echo Open your browser to:
echo   - Website: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py
