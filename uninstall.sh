#!/bin/bash
set -e

USER_BIN="$HOME/.local/bin"

rm -f "$USER_BIN/pull"
rm -f "$USER_BIN/push"
rm -f "$USER_BIN/send"
rm -f "$USER_BIN/server"

echo "Desinstalação concluída"
