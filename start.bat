
@echo off
title MBH DNS FINDER
cd /d "%~dp0"
color 0

where py >nul 2>&1
if not errorlevel 1 (
    set "PY=py -3"
) else (
    set "PY=python"
)

%PY% --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python non trovato.
    echo Installa Python e riprova.
    pause
    exit /b 1
)

%PY% -c "import dns.resolver" >nul 2>&1

if errorlevel 1 (
    echo [MBH] Installing DNS dependencies...
    %PY% -m pip install dnspython

    if errorlevel 1 (
        echo [ERROR] Installazione fallita.
        pause
        exit /b 1
    )
)

%PY% main.py

pause
