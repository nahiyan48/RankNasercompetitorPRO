@echo off
title Competitor Keyword & Article Tracker
chcp 65001 >nul
cls

echo =====================================================================
echo           COMPETITOR KEYWORD & ARTICLE TRACKER (PRO v1.0)
echo =====================================================================
echo.

set "PY_EXE="

:: 1. Check direct Python in AppData
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)

:: 2. Check py launcher in AppData
if not defined PY_EXE (
    if exist "%LOCALAPPDATA%\Programs\Python\Launcher\py.exe" (
        set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Launcher\py.exe"
    )
)

:: 3. Check PATH
if not defined PY_EXE (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set "PY_EXE=py"
    )
)

if not defined PY_EXE (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "PY_EXE=python"
    )
)

if not defined PY_EXE (
    echo [ERROR] Python not found in system!
    echo Please install Python 3.12 or check PATH.
    echo.
    pause
    exit /b 1
)

echo [*] Python located: "%PY_EXE%"
echo [*] Launching Tracker...
echo.

"%PY_EXE%" "%~dp0tracker.py"

echo.
echo =====================================================================
echo Execution finished.
pause
