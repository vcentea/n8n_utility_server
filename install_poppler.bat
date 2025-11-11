@echo off
echo ========================================
echo  Poppler Windows Installer
echo ========================================
echo.

echo This script will download and install Poppler for Windows.
echo.
pause

REM Create temp directory
set "TEMP_DIR=%TEMP%\poppler_install"
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

REM Download Poppler
echo Downloading Poppler (Release-24.08.0-0)...
echo Please wait, this may take a moment...
echo.

curl -L "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip" -o "%TEMP_DIR%\poppler.zip"

if errorlevel 1 (
    echo.
    echo ERROR: Download failed!
    echo Please download manually from: https://github.com/oschwartz10612/poppler-windows/releases
    echo Extract to C:\poppler and update your .env file
    pause
    exit /b 1
)

echo.
echo Download complete!
echo.

REM Extract to C:\poppler
echo Extracting to C:\poppler...
if exist "C:\poppler" (
    echo WARNING: C:\poppler already exists. Removing old version...
    rd /s /q "C:\poppler"
)

powershell -Command "Expand-Archive -Path '%TEMP_DIR%\poppler.zip' -DestinationPath '%TEMP_DIR%\extracted' -Force"
move "%TEMP_DIR%\extracted\poppler-24.08.0" "C:\poppler"

REM Cleanup
rd /s /q "%TEMP_DIR%"

REM Verify installation
if exist "C:\poppler\Library\bin\pdftoppm.exe" (
    echo.
    echo ========================================
    echo  Installation Successful!
    echo ========================================
    echo.
    echo Poppler is installed at: C:\poppler\Library\bin
    echo.
    echo The .env file will be updated automatically...
    echo.
    
    REM Update .env file to remove quotes and set correct path
    powershell -Command "(Get-Content .env) -replace '\"', '' | Set-Content .env"
    powershell -Command "(Get-Content .env) -replace 'POPPLER_PATH=.*', 'POPPLER_PATH=C:\poppler\Library\bin' | Set-Content .env"
    
    echo .env file updated!
    echo.
    echo You can now run: start_local.bat
    echo.
) else (
    echo.
    echo ERROR: Installation failed!
    echo pdftoppm.exe not found in expected location.
    echo Please install manually from: https://github.com/oschwartz10612/poppler-windows/releases
    pause
    exit /b 1
)

pause

