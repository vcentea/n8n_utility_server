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
set "POPPLER_PATH="
for /f "usebackq tokens=1,* delims==" %%A in (`findstr /b /i "PORT=" .env`) do set "PORT=%%B"
for /f "usebackq tokens=1,* delims==" %%A in (`findstr /b /i "POPPLER_PATH=" .env`) do set "POPPLER_PATH=%%B"
set "PORT=!PORT:"=%!"
if "!PORT!"=="" set "PORT=2277"
if not "!POPPLER_PATH!"=="" (
    set "POPPLER_PATH=!POPPLER_PATH:"=%!"
    if exist "!POPPLER_PATH!" (
        echo Adding POPPLER_PATH to PATH: !POPPLER_PATH!
        set "PATH=!POPPLER_PATH!;!PATH!"
    ) else (
        echo WARNING: POPPLER_PATH is set but directory does not exist: !POPPLER_PATH!
    )
)

echo Checking for virtual environment...
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting server on http://localhost:!PORT!
echo API Documentation: http://localhost:!PORT!/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --host 0.0.0.0 --port !PORT! --reload

