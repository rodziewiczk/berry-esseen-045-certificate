@echo off
setlocal
cd /d "%~dp0"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0finalize_publication.ps1"
if errorlevel 1 (
    echo ERROR: publication finalization failed.
    exit /b 2
)

exit /b 0
