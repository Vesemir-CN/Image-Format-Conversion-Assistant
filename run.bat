@echo off
REM Image Format Converter Launcher
REM Use Python 3 to run the application

REM Check for Python 3
py -3 --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 is not installed or not accessible
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Run the application with Python 3
py -3 main.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start the application
    echo Please make sure all dependencies are installed:
    echo   pip install -r requirements.txt
    pause
)
