#!/bin/bash
set -e

USER_BIN="$HOME/.local/bin"

for f in pull push send server; do
    if [ -f "$USER_BIN/$f" ]; then
        rm "$USER_BIN/$f"
        echo "removido: $f"
    else
        echo "não encontrado: $f"
    fi
done

echo "Desinstalação concluída."
