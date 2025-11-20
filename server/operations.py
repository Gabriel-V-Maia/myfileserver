import socket
import os
from pathlib import Path
import hashlib
from utils import Logger

logger = Logger("[Operations]")


class ServerOperations:
    # ---------------- Push ----------------
    def _push(self, conn: socket.socket, headers: dict):
        """
        Recebe headers do cliente e múltiplos arquivos
        """
        try:
            count = int(headers.get("COUNT", "0"))
            folder = headers.get("DIR", "Docs")
            folder_path = self.STORAGE_DIR / folder
            folder_path.mkdir(parents=True, exist_ok=True)

            for _ in range(count):
                file_hdr = self._read_headers(conn)
                name = file_hdr["NAME"]
                size = int(file_hdr["SIZE"])
                expected_ck = file_hdr.get("CHECK", None)

                path = folder_path / name
                received = 0
                data = b""

                while received < size:
                    chunk = conn.recv(min(4096, size - received))
                    if not chunk:
                        break
                    data += chunk
                    received += len(chunk)

                actual_ck = hashlib.sha256(data).hexdigest()
                if expected_ck and actual_ck != expected_ck:
                    logger.error(f"[!] Checksum incorreto: {name}")
                    conn.sendall(f"STATUS=erro\nMSG=checksum incorreto\nENDHDR\n".encode())
                    continue

                with open(path, "wb") as f:
                    f.write(data)
                logger.info(f"[+] Arquivo armazenado: {path}")

                conn.sendall(b"STATUS=ok\nENDHDR\n")

        except Exception as e:
            logger.error(f"[!] Erro em _push: {e}")
            conn.sendall(f"STATUS=erro\nMSG={e}\nENDHDR\n".encode())

    # ---------------- Pull ----------------
    def _pull(self, conn: socket.socket, headers: dict):
        """
        Envia múltiplos arquivos solicitados pelo cliente
        """
        try:
            count = int(headers.get("COUNT", "0"))
            folder = headers.get("DIR", "Docs")
            folder_path = self.STORAGE_DIR / folder

            if not folder_path.exists():
                conn.sendall(f"STATUS=erro\nMSG=pasta nao encontrada\nENDHDR\n".encode())
                return

            for _ in range(count):
                file_hdr = self._read_headers(conn)
                name = file_hdr["NAME"]
                path = folder_path / name

                if not path.exists() or not path.is_file():
                    conn.sendall(f"STATUS=erro\nMSG=arquivo nao encontrado: {name}\nENDHDR\n".encode())
                    continue

                size = path.stat().st_size
                cksum = hashlib.sha256(path.read_bytes()).hexdigest()

                hdr = {
                    "STATUS": "ok",
                    "NAME": name,
                    "SIZE": str(size),
                    "CHECK": cksum
                }
                self._send_headers(conn, hdr)

                # Envia arquivo
                with open(path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        conn.sendall(chunk)

        except Exception as e:
            logger.error(f"[!] Erro em _pull: {e}")
            conn.sendall(f"STATUS=erro\nMSG={e}\nENDHDR\n".encode())

    # ---------------- Helpers ----------------
    def _send_headers(self, conn: socket.socket, headers: dict):
        for k, v in headers.items():
            conn.sendall(f"{k}={v}\n".encode())
        conn.sendall(b"ENDHDR\n")


