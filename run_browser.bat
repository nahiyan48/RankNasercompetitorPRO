@echo off
title Competitor Keyword Tracker & SEO Spy Dashboard
chcp 65001 >nul
cls

echo =====================================================================
echo           COMPETITOR TRACKER & SEO SPY - WEB DASHBOARD
echo =====================================================================
echo.

set "PY_EXE="
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)
if not defined PY_EXE (
    where python >nul 2>nul
    if %errorlevel% equ 0 set "PY_EXE=python"
)

echo [*] Starting Web Dashboard server...
echo [*] Opening your browser at http://localhost:5000 ...
echo.
echo ---------------------------------------------------------------------
echo  [!] Instructions:
echo  This console window acts as the background server engine.
echo  Keep this window open (minimized) while using the dashboard.
echo  Close this window when you are completely finished.
echo ---------------------------------------------------------------------
echo.

:: Automatically open default browser
start "" "http://localhost:5000"

:: Start the web server
"%PY_EXE%" "%~dp0web_app.py"

pause
