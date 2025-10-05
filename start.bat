@echo off
echo Smart Repository Assistant - Windows Startup Script
echo ====================================================

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

:: Run setup if .env doesn't exist
if not exist ".env" (
    echo Running initial setup...
    python setup.py
    if errorlevel 1 (
        echo Error: Setup failed
        pause
        exit /b 1
    )
)

:: Run system test
echo Running system test...
python test_system.py
if errorlevel 1 (
    echo Warning: System test found issues
    echo Please check your configuration
    pause
)

echo.
echo ====================================================
echo Choose what to start:
echo 1. Webhook Server (Flask App)
echo 2. Analytics Dashboard (Streamlit)
echo 3. Both (in separate windows)
echo 4. Exit
echo ====================================================
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Starting webhook server...
    python app.py
) else if "%choice%"=="2" (
    echo Starting analytics dashboard...
    streamlit run dashboard.py
) else if "%choice%"=="3" (
    echo Starting both services...
    start "Smart Repo Assistant - Webhook Server" cmd /c "call .venv\Scripts\activate.bat && python app.py && pause"
    start "Smart Repo Assistant - Dashboard" cmd /c "call .venv\Scripts\activate.bat && streamlit run dashboard.py && pause"
    echo Both services started in separate windows
    pause
) else if "%choice%"=="4" (
    echo Goodbye!
) else (
    echo Invalid choice
    pause
)

pause