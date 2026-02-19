@echo off
REM Simplified server start script for Scientific Image Processing Assistant

REM Check for Python 3
py -3 --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 is not installed or not accessible
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Create necessary directories
mkdir uploads 2>nul
mkdir outputs 2>nul

REM Run the backend server
echo Starting Scientific Image Processing Assistant...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server

py -3 -m flask run --host=0.0.0.0 --port=5000

if errorlevel 1 (
    echo.
    echo Error: Failed to start the server
    echo Please check the error message above
    pause
)
