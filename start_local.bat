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

