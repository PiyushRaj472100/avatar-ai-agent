@echo off
echo Starting Avatar AI Agent...
echo.

REM Activate virtual environment
call .venv\Scripts\activate

REM Check if activation was successful
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    echo Please make sure .venv exists and run setup first
    pause
    exit /b 1
)

echo Virtual environment activated successfully
echo.

REM Start the application
echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --reload

pause
