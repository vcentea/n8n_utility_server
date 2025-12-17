@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Docker Deployment Update Script
echo ========================================
echo.

REM Check if docker-compose is installed
where docker-compose >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    where docker >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Docker or docker-compose is not installed!
        echo Please install Docker first.
        exit /b 1
    )
)

REM Determine docker compose command
set "DOCKER_COMPOSE_CMD=docker-compose"
where docker-compose >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    docker compose version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set "DOCKER_COMPOSE_CMD=docker compose"
    ) else (
        echo ERROR: Could not find docker-compose or docker compose command!
        exit /b 1
    )
)

echo [1/5] Backing up current .env file...
if exist .env (
    copy /Y .env .env.backup >nul
    echo .env backed up to .env.backup
) else (
    echo WARNING: No .env file found. Will create from .env.example after pull.
)
echo.

echo [2/5] Pulling latest code from git...
if exist .git (
    REM Stash any local changes to prevent conflicts
    git stash push -m "Auto-stash before update %date%_%time%"
    
    REM Pull latest changes
    git pull origin main
    
    echo Latest code pulled successfully!
) else (
    echo ERROR: Not a git repository!
    echo Please run this script from the project root directory.
    exit /b 1
)
echo.

echo [3/5] Checking .env configuration...
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env >nul
    echo IMPORTANT: Please edit .env and set your API_KEY!
    echo After setting API_KEY, run this script again.
    exit /b 0
)

REM Restore API_KEY from backup if it exists
if exist .env.backup (
    for /f "tokens=1,* delims==" %%a in ('findstr /r "^API_KEY=" .env.backup 2^>nul') do (
        set "OLD_API_KEY=%%b"
    )
    
    if defined OLD_API_KEY (
        REM Create temp file with updated API_KEY
        (for /f "delims=" %%i in (.env) do (
            set "line=%%i"
            if "!line:~0,8!"=="API_KEY=" (
                echo API_KEY=!OLD_API_KEY!
            ) else (
                echo %%i
            )
        )) > .env.tmp
        move /Y .env.tmp .env >nul
        echo API_KEY restored from backup
    )
)

REM Check if API_KEY is set
for /f "tokens=1,* delims==" %%a in ('findstr /r "^API_KEY=" .env 2^>nul') do (
    set "API_KEY=%%b"
)

if not defined API_KEY (
    echo WARNING: API_KEY is not set!
    echo Please edit .env and set a secure API_KEY.
    set /p "CONTINUE=Continue anyway? (y/n) "
    if /i not "!CONTINUE!"=="y" exit /b 1
) else if "!API_KEY!"=="your-secret-key-here" (
    echo WARNING: API_KEY is using default value!
    echo Please edit .env and set a secure API_KEY.
    set /p "CONTINUE=Continue anyway? (y/n) "
    if /i not "!CONTINUE!"=="y" exit /b 1
)
echo.

echo [4/5] Stopping current containers...
%DOCKER_COMPOSE_CMD% down
echo Containers stopped
echo.

echo [5/5] Building and starting containers...
%DOCKER_COMPOSE_CMD% build --no-cache
%DOCKER_COMPOSE_CMD% up -d

echo.
echo Waiting for service to start...
timeout /t 3 /nobreak >nul

REM Check if container is running
%DOCKER_COMPOSE_CMD% ps | findstr "Up" >nul
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo  Update Complete!
    echo ========================================
    echo.
    echo Service is running:
    %DOCKER_COMPOSE_CMD% ps
    echo.
    echo To view logs:
    echo   %DOCKER_COMPOSE_CMD% logs -f
    echo.
    echo To stop the service:
    echo   %DOCKER_COMPOSE_CMD% down
) else (
    echo ========================================
    echo  ERROR: Container failed to start!
    echo ========================================
    echo.
    echo Check logs with:
    echo   %DOCKER_COMPOSE_CMD% logs
    exit /b 1
)




