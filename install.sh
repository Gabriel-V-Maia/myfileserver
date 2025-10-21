#!/bin/bash
set -e

ROOT="$(pwd)"
CLIENT="$ROOT/client"
DIST="$CLIENT/dist"
USER_BIN="$HOME/.local/bin"

mkdir -p "$USER_BIN"

python3 -m pip install --user pyinstaller

cd "$CLIENT"
python3 -m PyInstaller --onefile pull.py
python3 -m PyInstaller --onefile push.py
python3 -m PyInstaller --onefile send.py
cd "$ROOT"

cp "$DIST/pull" "$USER_BIN/pull"
cp "$DIST/push" "$USER_BIN/push"
cp "$DIST/send" "$USER_BIN/send"

export PATH="$PATH:$USER_BIN"
echo "Instalação concluída. Agora você pode usar: pull, push, send"
