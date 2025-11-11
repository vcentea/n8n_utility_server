@echo off
setlocal EnableDelayedExpansion
echo Testing PDF-to-Images Endpoint
echo.

if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure it.
    pause
    exit /b 1
)

echo Reading configuration from .env file...
set "PORT="
set "ENV_API_KEY="
for /f "usebackq tokens=1,* delims==" %%A in (`findstr /b /i "PORT=" .env`) do set "PORT=%%B"
for /f "usebackq tokens=1,* delims==" %%A in (`findstr /b /i "API_KEY=" .env`) do set "ENV_API_KEY=%%B"
set "PORT=!PORT:"=%!"
set "ENV_API_KEY=!ENV_API_KEY:"=%!"
if "!PORT!"=="" set "PORT=2277"

if "!ENV_API_KEY!"=="" (
    set /p "API_KEY=Enter your API_KEY: "
    set "API_KEY=!API_KEY:"=%!"
) else (
    echo Using API_KEY from .env file
    set "API_KEY=!ENV_API_KEY!"
)

set /p "PDF_FILE=Enter path to PDF file: "
set "PDF_FILE=!PDF_FILE:"=%!"

if not exist "!PDF_FILE!" (
    echo ERROR: File not found: !PDF_FILE!
    pause
    exit /b 1
)

echo.
echo Sending request to http://localhost:!PORT!/api/v1/pdf-to-images...
echo.

curl -X POST "http://localhost:!PORT!/api/v1/pdf-to-images" ^
  -H "x-api-key: !API_KEY!" ^
  -F "file=@\"!PDF_FILE!\";type=application/pdf"

echo.
echo.
pause

