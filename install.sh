#!/bin/bash
set -e

ROOT="$(pwd)"
CLIENT="$ROOT/client"
SERVER="$ROOT/server"
DIST_CLIENT="$CLIENT/dist"
DIST_SERVER="$SERVER/dist"
USER_BIN="$HOME/.local/bin"

mkdir -p "$USER_BIN"

python3 -m pip install --break-system-packages --user pyinstaller

cd "$CLIENT"
python3 -m PyInstaller --onefile pull.py
python3 -m PyInstaller --onefile push.py
python3 -m PyInstaller --onefile send.py
cd "$ROOT"

cd "$SERVER"
python3 -m PyInstaller --onefile server.py
cd "$ROOT"

cp "$DIST_CLIENT/pull" "$USER_BIN/pull"
cp "$DIST_CLIENT/push" "$USER_BIN/push"
cp "$DIST_CLIENT/send" "$USER_BIN/send"
cp "$DIST_SERVER/server" "$USER_BIN/server"

chmod +x "$USER_BIN/pull" "$USER_BIN/push" "$USER_BIN/send" "$USER_BIN/server"

export PATH="$PATH:$USER_BIN"
echo "Instalação concluída. Agora você pode usar: pull, push, send, server"

