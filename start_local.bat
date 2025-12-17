@echo off
setlocal EnableDelayedExpansion
echo Starting Utility Service Platform...
echo.

if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure it.
    pause
    exit /b 1
)

echo Reading configuration from .env file...
set "PORT="
for /f "usebackq tokens=1,* delims==" %%A in (`findstr /b /i "PORT=" .env`) do set "PORT=%%B"
set "PORT=!PORT:"=%!"
if "!PORT!"=="" set "PORT=2277"

echo Checking for virtual environment...
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

echo Verifying virtual environment...
if not exist venv\Scripts\python.exe (
    echo ERROR: Virtual environment is corrupted!
    echo Please delete the venv folder and run this script again.
    pause
    exit /b 1
)

echo Installing/updating dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo Starting server on http://localhost:!PORT!
echo API Documentation: http://localhost:!PORT!/docs
echo.
echo Press Ctrl+C to stop the server
echo.

venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port !PORT! --reload

