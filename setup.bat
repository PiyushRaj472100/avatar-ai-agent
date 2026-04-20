@echo off
echo Setting up Avatar AI Agent...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

echo Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created successfully
echo.

REM Activate virtual environment and install dependencies
echo Installing dependencies...
call .venv\Scripts\activate
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo IMPORTANT: Before running the app:
echo 1. Get your Gemini API key from: https://makersuite.google.com/app/apikey
echo 2. Edit .env file and replace the API key
echo 3. Run 'run.bat' to start the application
echo.
echo Next steps:
echo - Edit .env file with your Gemini API key
echo - Run 'run.bat' to start Avatar AI Agent
echo - Visit http://localhost:8000/docs for API documentation
echo.
pause
