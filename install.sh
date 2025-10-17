#!/bin/bash

if [ "$EUID" -ne 0 ]; then 
    echo "Este script requer privilégios de root"
    sudo "$0"
    exit $?
fi

cd "$(dirname "$0")"

echo "[+] Compilando server..."
python3 -m PyInstaller --onefile server/server.py
if [ $? -ne 0 ]; then
    echo "[!] Erro ao compilar server"
    exit 1
fi

echo "[+] Compilando client..."
python3 -m PyInstaller --onefile client/client.py
if [ $? -ne 0 ]; then
    echo "[!] Erro ao compilar client"
    exit 1
fi

echo "[+] Copiando executaveis para /usr/local/bin/..."
cp dist/server /usr/local/bin/
cp dist/client /usr/local/bin/
chmod +x /usr/local/bin/server
chmod +x /usr/local/bin/client

echo "[+] Instalacao completa!"
echo "Use 'server' e 'client' em qualquer lugar"