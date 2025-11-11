@echo off
echo Testing PDF-to-Images Endpoint
echo.

set /p API_KEY="Enter your API_KEY: "
set /p PDF_FILE="Enter path to PDF file: "

if not exist "%PDF_FILE%" (
    echo ERROR: File not found: %PDF_FILE%
    pause
    exit /b 1
)

echo.
echo Sending request...
echo.

curl -X POST http://localhost:8080/api/v1/pdf-to-images ^
  -H "x-api-key: %API_KEY%" ^
  -F "file=@%PDF_FILE%"

echo.
echo.
pause

