@echo off
setlocal EnableDelayedExpansion
echo ========================================
echo  Utility Service Platform Setup
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env and set your API_KEY before running!
    echo.
)

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.12+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Python found: 
python --version
echo.

REM Check for Poppler
echo [2/4] Checking for Poppler...
where pdftoppm >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Poppler is NOT installed!
    echo.
    echo Poppler is REQUIRED for PDF conversion. Choose an option:
    echo.
    echo   Option 1: Install via Chocolatey (Recommended if you have Choco)
    echo             choco install poppler
    echo.
    echo   Option 2: Manual Download
    echo             1. Download: https://github.com/oschwartz10612/poppler-windows/releases
    echo             2. Extract to C:\poppler
    echo             3. Run this setup again
    echo.
    choice /C YN /M "Do you want to attempt Chocolatey installation now?"
    if errorlevel 2 goto :skip_choco
    if errorlevel 1 goto :install_choco
    
    :install_choco
    where choco >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ERROR: Chocolatey is not installed!
        echo Install Chocolatey from: https://chocolatey.org/install
        echo Then run this setup again.
        pause
        exit /b 1
    )
    echo Installing Poppler via Chocolatey...
    choco install poppler -y
    if errorlevel 1 (
        echo.
        echo ERROR: Chocolatey installation failed!
        echo Please install manually from: https://github.com/oschwartz10612/poppler-windows/releases
        pause
        exit /b 1
    )
    echo Poppler installed successfully!
    goto :poppler_done
    
    :skip_choco
    echo.
    echo Please install Poppler manually and run this setup again.
    echo See POPPLER_SETUP.md for detailed instructions.
    pause
    exit /b 1
) else (
    echo Poppler found: 
    where pdftoppm
)

:poppler_done
echo.

REM Create virtual environment
echo [3/4] Setting up Python virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

REM Install Python dependencies
echo [4/4] Installing Python dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo.

echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Edit .env and set your API_KEY
echo   2. Run: start_local.bat
echo.
echo For Docker deployment (zero configuration):
echo   docker-compose up -d
echo.
pause

