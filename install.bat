@echo off
setlocal

set ROOT=%~dp0
set CLIENT=%ROOT%client
set DIST=%CLIENT%\dist
set USER_BIN=%USERPROFILE%\myfileserver\bin

if not exist "%USER_BIN%" mkdir "%USER_BIN%"

python -m pip install --user pyinstaller

cd "%CLIENT%"
python -m PyInstaller --onefile pull.py
python -m PyInstaller --onefile push.py
python -m PyInstaller --onefile send.py
cd "%ROOT%"

if not exist "%DIST%\pull.exe" (
    exit /b
)

copy /Y "%DIST%\pull.exe" "%USER_BIN%\pull.exe"
copy /Y "%DIST%\push.exe" "%USER_BIN%\push.exe"
copy /Y "%DIST%\send.exe" "%USER_BIN%\send.exe"

setx PATH "%PATH%;%USER_BIN%"

powershell -Command "$env:PATH += ';%USER_BIN%'"

echo Tudo pronto!

pause
