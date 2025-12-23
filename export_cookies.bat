@echo off
REM Export YouTube cookies from your local browser
REM This script uses yt-dlp to extract cookies from your browser

echo ================================================================
echo   Exporting YouTube Cookies from Browser
echo ================================================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first to create the venv.
    echo.
    pause
    exit /b 1
)

REM Check if yt-dlp is available
where yt-dlp >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] yt-dlp not found in venv!
    echo.
    echo The virtual environment might not be set up correctly.
    echo Please run setup.bat first.
    echo.
    pause
    exit /b 1
)

echo Select your browser:
echo   1. Firefox (RECOMMENDED - works best on Windows)
echo   2. Chrome (may have DPAPI issues)
echo   3. Edge (may have DPAPI issues)
echo.
set /p browser_choice="Enter choice (1-3): "

if "%browser_choice%"=="1" set BROWSER=firefox
if "%browser_choice%"=="2" set BROWSER=chrome
if "%browser_choice%"=="3" set BROWSER=edge

if "%BROWSER%"=="" (
    echo Invalid choice!
    pause
    exit /b 1
)

echo.
echo Extracting cookies from %BROWSER%...
echo (This may take a moment...)
echo.
echo NOTE: If you see "DPAPI" errors, use the browser extension method instead.
echo.

REM Use a simple YouTube URL to trigger cookie extraction
yt-dlp --cookies-from-browser %BROWSER% --cookies cookies.txt --skip-download "https://www.youtube.com/watch?v=jNQXAC9IVRw"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo   SUCCESS! Cookies exported to: cookies.txt
    echo ================================================================
    echo.
    echo Next steps:
    echo   1. Copy cookies.txt to your production server:
    echo      scp cookies.txt user@server:/path/to/project/
    echo.
    echo   2. Add to production .env:
    echo      YOUTUBE_COOKIES_PATH=/app/cookies.txt
    echo      YOUTUBE_COOKIES_FILE=./cookies.txt
    echo.
    echo   3. Rebuild container:
    echo      ./update_docker.sh
    echo.
) else (
    echo.
    echo ================================================================
    echo [ERROR] Failed to export cookies!
    echo ================================================================
    echo.
    echo If you saw "DPAPI" errors:
    echo   - This is a Windows encryption limitation
    echo   - yt-dlp cannot decrypt Edge/Chrome cookies on Windows
    echo   - SOLUTION: Use browser extension instead (see below)
    echo.
    echo Other common issues:
    echo   1. Browser is still running (close completely via Task Manager)
    echo   2. Browser database is locked
    echo.
    echo ================================================================
    echo RECOMMENDED: Use Browser Extension (Works 100%% of the time)
    echo ================================================================
    echo.
    echo Steps:
    echo   1. Install "Get cookies.txt LOCALLY" extension:
    echo      Edge:   https://microsoftedge.microsoft.com/addons/detail/hbihflbpfdeopgegegknkfplckkomdja
    echo      Chrome: https://chrome.google.com/webstore/detail/cclelndahbckbenkjhflpdbgdldlbecc
    echo.
    echo   2. Go to YouTube.com (make sure you're logged in)
    echo   3. Click extension icon
    echo   4. Click "Export"
    echo   5. Save as "cookies.txt" in this folder
    echo.
    echo See COOKIE_EXPORT_GUIDE.md for detailed instructions.
    echo.
)

pause

