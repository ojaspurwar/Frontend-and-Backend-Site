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

echo [1/2] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/2] Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Server is starting!
echo ========================================
echo.
echo Local access:
echo   - Website: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo   - Admin: http://localhost:8000/admin/login
echo.
echo Public tunnel will start below...
echo.

REM Start server in background
start "" python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

REM Wait for server to start
timeout /t 2 /nobreak

REM Start tunnel with localtunnel
echo.
echo ========================================
echo Starting public tunnel...
echo ========================================
echo.
npx localtunnel --port 8000 --subdomain=portfolio-%RANDOM%
