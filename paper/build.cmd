@echo off
setlocal
cd /d "%~dp0"

if not exist "..\output\pdf" mkdir "..\output\pdf"
if errorlevel 1 (
    echo ERROR: could not create ..\output\pdf.
    exit /b 2
)
if not exist "..\tmp\paper-build" mkdir "..\tmp\paper-build"
if errorlevel 1 (
    echo ERROR: could not create ..\tmp\paper-build.
    exit /b 2
)

where tectonic >nul 2>nul
if not errorlevel 1 (
    tectonic --keep-logs --outdir "..\tmp\paper-build" "berry_esseen_045.tex"
    if errorlevel 1 exit /b 2
    move /y "..\tmp\paper-build\berry_esseen_045.pdf" "..\output\pdf\berry_esseen_045_publication.pdf" >nul
    if errorlevel 1 exit /b 2
    echo MANUSCRIPT READY: output\pdf\berry_esseen_045_publication.pdf
    exit /b 0
)

if exist "..\tmp\pdfs\toolchain\tectonic.exe" (
    "..\tmp\pdfs\toolchain\tectonic.exe" --keep-logs --outdir "..\tmp\paper-build" "berry_esseen_045.tex"
    if errorlevel 1 exit /b 2
    move /y "..\tmp\paper-build\berry_esseen_045.pdf" "..\output\pdf\berry_esseen_045_publication.pdf" >nul
    if errorlevel 1 exit /b 2
    echo MANUSCRIPT READY: output\pdf\berry_esseen_045_publication.pdf
    exit /b 0
)

where latexmk >nul 2>nul
if not errorlevel 1 (
    latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir="..\tmp\paper-build" "berry_esseen_045.tex"
    if errorlevel 1 exit /b 2
    move /y "..\tmp\paper-build\berry_esseen_045.pdf" "..\output\pdf\berry_esseen_045_publication.pdf" >nul
    if errorlevel 1 exit /b 2
    echo MANUSCRIPT READY: output\pdf\berry_esseen_045_publication.pdf
    exit /b 0
)

echo ERROR: install Tectonic or latexmk to build the manuscript.
exit /b 2
