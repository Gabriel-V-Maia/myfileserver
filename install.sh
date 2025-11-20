#!/bin/bash
set -e

ROOT="$(pwd)"
CLIENT="$ROOT/client"
SERVER="$ROOT/server"
DIST_CLIENT="$CLIENT/dist"
DIST_SERVER="$SERVER/dist"

CONFIG_ROOT="$HOME/myfileserverconfigs"
BIN_PATH="$CONFIG_ROOT/bins"
ENV_FILE="$CONFIG_ROOT/.env"

echo "Criando estrutura de diretórios..."
mkdir -p "$BIN_PATH"

echo "Instalando PyInstaller..."
python3 -m pip install --break-system-packages --user pyinstaller 2>/dev/null || python3 -m pip install --user pyinstaller

echo "PyInstaller Instalado!"
sleep 2
clear

echo "[*] Iniciando build dos executáveis..."

echo "Compilando cliente..."
cd "$CLIENT"

python3 -m PyInstaller --onefile filepull.py --name pull \
    --hidden-import=dotenv --hidden-import=python-dotenv

python3 -m PyInstaller --onefile filesend.py --name send \
    --hidden-import=dotenv --hidden-import=python-dotenv

echo "[OK] Cliente compilado"
sleep 2
clear

echo "Compilando servidor..."
cd "$SERVER"
python3 -m PyInstaller --onefile main.py --name server

echo "[OK] Servidor compilado!"
sleep 2
clear

echo "Verificando bins..."

cd "$ROOT"

if [ ! -f "$DIST_CLIENT/pull" ]; then
    echo "Erro: executável 'pull' não encontrado"
    exit 1
fi

if [ ! -f "$DIST_CLIENT/send" ]; then
    echo "Erro: executável 'send' não encontrado"
    exit 1
fi

if [ ! -f "$DIST_SERVER/server" ]; then
    echo "Erro: executável 'server' não encontrado"
    exit 1
fi

echo "Copiando executáveis..."
cp "$DIST_CLIENT/pull" "$BIN_PATH/pull"
cp "$DIST_CLIENT/send" "$BIN_PATH/send"
cp "$DIST_SERVER/server" "$BIN_PATH/server"

chmod +x "$BIN_PATH/pull" "$BIN_PATH/send" "$BIN_PATH/server"

echo ""

if [ -f "$ENV_FILE" ]; then
    echo "Arquivo .env já existe."
    read -p "Deseja reconfigurar o IP do servidor? (s/N): " reconfig
    if [[ "$reconfig" =~ ^[sS]$ ]]; then
        read -p "Digite o IP do servidor (ex: 192.168.1.100): " server_ip
        echo "server_ip=$server_ip" > "$ENV_FILE"
        echo "Arquivo .env atualizado!"
    else
        echo "Mantendo configuração existente."
    fi
else
    echo "Configuração do servidor:"
    read -p "Digite o IP do servidor (ex: 192.168.1.100): " server_ip
    echo "server_ip=$server_ip" > "$ENV_FILE"
    echo "Arquivo .env criado em: $ENV_FILE"
fi

SHELL_RC=""
if [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "$BIN_PATH" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# myfileserver" >> "$SHELL_RC"
        echo "export PATH=\"\$PATH:$BIN_PATH\"" >> "$SHELL_RC"
        echo "PATH atualizado em $SHELL_RC"
    fi
fi

export PATH="$PATH:$BIN_PATH"

sleep 2
clear

echo ""
echo "====================================="
echo "Instalação concluída com sucesso!"
echo "====================================="
echo ""
echo "Comandos disponíveis:"
echo "  - pull <arquivo>"
echo "  - send <arquivo1> <arquivo2> ... [destinatário]"
echo "  - server"
echo ""
echo "Configuração em: $CONFIG_ROOT"
echo ""
echo "OBS: Execute 'source $SHELL_RC' ou reinicie o terminal para usar os comandos!"
echo ""


