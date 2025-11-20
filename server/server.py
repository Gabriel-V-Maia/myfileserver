import socket
import os
from pathlib import Path
from utils import Logger
from operations import ServerOperations

logger = Logger("[Server]")


class FileServer(ServerOperations):
    def __init__(self, HOST="0.0.0.0", PORT=6000, STORAGEDIR=None):
        self.HOST = HOST
        self.PORT = PORT
        self.STORAGE_DIR = Path(STORAGEDIR or Path.home() / "fileserver")
        self.STORAGE_DIR.mkdir(exist_ok=True)
        self.active_connections = {}

    @property
    def get_active_connections(self):
        return self.active_connections

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))
            s.listen()
            logger.info(f"[+] Servidor iniciado em {self.HOST}:{self.PORT}")
            logger.info(f"[i] Diretório de storage: {self.STORAGE_DIR}")

            while True:
                conn, addr = s.accept()
                with conn:
                    self.active_connections[addr] = conn
                    logger.warn(f"[*] Cliente conectado: {addr}")
                    try:
                        self.handle(conn, addr)
                    except Exception as e:
                        logger.error(f"[!] Erro durante handle: {e}")
                    finally:
                        del self.active_connections[addr]

    def handle(self, conn: socket.socket, addr: tuple):
        """
        Recebe headers do cliente, identifica comando e chama _push ou _pull
        """
        try:
            headers = self._read_headers(conn)
            cmd_type = headers.get("CMD", "").lower()

            if not cmd_type:
                conn.sendall(b"ERRO=Comando vazio\nENDHDR\n")
                return

            match cmd_type:
                case "push":
                    self._push(conn, headers)
                case "pull":
                    self._pull(conn, headers)
                case _:
                    conn.sendall(b"ERRO=Comando invalido\nENDHDR\n")

        except Exception as e:
            logger.error(f"[!] Erro ao processar comando: {e}")
            try:
                conn.sendall(f"ERRO={e}\nENDHDR\n".encode())
            except:
                pass

    # ---------------- Helpers ----------------
    def _read_headers(self, conn: socket.socket):
        """
        Lê todos os headers até ENDHDR e retorna um dict
        """
        headers = {}
        buffer = ""
        while True:
            chunk = conn.recv(1024).decode()
            if not chunk:
                raise ConnectionError("Conexao perdida")
            buffer += chunk

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if line == "ENDHDR":
                    return headers
                if "=" in line:
                    k, v = line.split("=", 1)
                    headers[k] = v


