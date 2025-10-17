@echo off
setlocal enabledelayedexpansion

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Este script requer privilégios de administrador
    pause
    exit /b 1
)

cd /d "%~dp0"

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

echo [+] Copiando executaveis para C:\Windows\System32\...
copy dist\server.exe C:\Windows\System32\
copy dist\client.exe C:\Windows\System32\

echo [+] Instalacao completa!
echo Use 'server' e 'client' em qualquer lugar
pause