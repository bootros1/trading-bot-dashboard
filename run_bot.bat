@echo off
echo Starting Forex Trading Bot...
echo Time: %date% %time%
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and ensure it's added to PATH
    pause
    exit /b 1
)

REM Check if config.py exists
if not exist "config.py" (
    echo ERROR: config.py not found
    echo Please ensure you're in the correct directory
    pause
    exit /b 1
)

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

echo Running trading bot...
python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Bot execution failed
    echo Check the logs in the logs/ directory for details
) else (
    echo.
    echo Bot execution completed successfully
)

echo.
echo Press any key to exit...
pause >nul 