@echo off
REM Canadian Weather Web App Launcher
REM This script starts the Flask web application

echo.
echo ========================================
echo    Canadian Weather Web App Launcher
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.6+ and try again.
    pause
    exit /b 1
)

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo Flask is not installed. Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Error: Failed to install dependencies.
        pause
        exit /b 1
    )
)

echo Starting Canadian Weather Web App...
echo.
echo The web app will open at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask application
python web_app.py

echo.
echo Web app has stopped.
pause
