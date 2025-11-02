#!/bin/bash
set -e

CONFIG_ROOT="$HOME/myfileserverconfigs"
BIN_PATH="$CONFIG_ROOT/bins"

echo "====================================="
echo "Desinstalando myfileserver..."
echo "====================================="

for rc_file in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$rc_file" ]; then
        if grep -q "$BIN_PATH" "$rc_file"; then
            echo "Removendo do PATH em $rc_file..."
            sed -i '/# myfileserver/d' "$rc_file"
            sed -i "\|export PATH=\"\$PATH:$BIN_PATH\"|d" "$rc_file"
            sed -i '/^$/N;/^\n$/d' "$rc_file"
        fi
    fi
done

if [ -d "$CONFIG_ROOT" ]; then
    echo "Removendo diretório de configuração..."
    rm -rf "$CONFIG_ROOT"
    echo "Diretório removido: $CONFIG_ROOT"
else
    echo "Diretório de configuração não encontrado."
fi

echo ""
echo "====================================="
echo "Desinstalação concluída!"
echo "====================================="
echo ""
