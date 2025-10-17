@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Este script requer privilégios de administrador
    echo Reexecutando como administrador...
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d \"%cd%\" ^&^& %~s0' -Verb RunAs"
    exit /b
)

echo [+] Compilando server...
python -m PyInstaller --onefile server/server.py
if errorlevel 1 (
    echo [!] Erro ao compilar server
    pause
    exit /b 1
)

echo [+] Compilando client...
python -m PyInstaller --onefile client/client.py
if errorlevel 1 (
    echo [!] Erro ao compilar client
    pause
    exit /b 1
)

echo [+] Copiando executaveis para PATH...
copy dist\server.exe C:\Windows\System32\ >nul
if errorlevel 1 (
    echo [!] Erro ao copiar server.exe
    pause
    exit /b 1
)

copy dist\client.exe C:\Windows\System32\ >nul
if errorlevel 1 (
    echo [!] Erro ao copiar client.exe
    pause
    exit /b 1
)

echo [+] Instalacao completa!
echo Use 'server' e 'client' em qualquer lugar
pause