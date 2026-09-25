@echo off
setlocal
cd /d "%~dp0"

where docker >nul 2>nul
if errorlevel 1 (
    echo ERROR: Docker Desktop is required and docker.exe is not on PATH.
    exit /b 2
)

docker compose version >nul 2>nul
if errorlevel 1 (
    echo ERROR: Docker Compose is not available.
    exit /b 2
)

docker info >nul 2>nul
if errorlevel 1 (
    echo ERROR: the Docker engine is not running or is not accessible.
    exit /b 2
)

set "RUNNING_VERIFY="
for /f "delims=" %%I in ('docker ps --filter "label=com.docker.compose.project=berry-esseen-045" --filter "label=com.docker.compose.service=verify" --format "{{.ID}}"') do set "RUNNING_VERIFY=%%I"
if defined RUNNING_VERIFY (
    echo ERROR: a Berry--Esseen verification container is already running: %RUNNING_VERIFY%
    echo Wait for it to finish; simultaneous runs would share artifacts.
    exit /b 2
)

if not exist "data\parameter_bank\manifest.json" (
    echo ERROR: data\parameter_bank is missing or incomplete.
    exit /b 2
)

if not exist "artifacts" mkdir "artifacts"
if errorlevel 1 (
    echo ERROR: could not create the artifacts directory.
    exit /b 2
)

docker compose run --build --rm verify
set "VERIFY_EXIT=%ERRORLEVEL%"

if not "%VERIFY_EXIT%"=="0" (
    echo VERIFICATION FAILED with exit code %VERIFY_EXIT%.
    exit /b %VERIFY_EXIT%
)

echo VERIFICATION COMPLETE: artifacts\certificate\verification.json
exit /b 0
