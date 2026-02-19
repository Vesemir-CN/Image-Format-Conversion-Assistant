@echo off
REM Scientific Image Processing Assistant - Backend Server

REM Check for Python 3
py -3 --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 is not installed or not accessible
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if all dependencies are installed
echo Checking dependencies...
py -3 -c "import flask, flask_cors, converter, file_processor" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    py -3 -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create upload and output directories
mkdir uploads 2>nul
mkdir outputs 2>nul

REM Run the backend server
echo Starting Scientific Image Processing Assistant...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server

py -3 app.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start the server
    echo Please check the error message above
    pause
)
