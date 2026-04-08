#!/bin/bash
# FastAPI Portfolio Website - Quick Start for Linux/Mac

echo ""
echo "========================================"
echo "FastAPI Portfolio Website Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt

echo "[4/5] Creating database..."
# Database will be created automatically on first run

echo "[5/5] Starting server..."
echo ""
echo "========================================"
echo "Server is running!"
echo "========================================"
echo ""
echo "Open your browser to:"
echo "  - Website: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 main.py
