import socket
import os
import hashlib

class FilePuller:
    def __init__(self, host="127.0.0.1", port=6000):
        self.host = host
        self.port = port

    # ---------------- Helpers ----------------
    def _connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        return s

    def _send_headers(self, conn, headers: dict):
        for k, v in headers.items():
            conn.sendall(f"{k}={v}\n".encode())
        conn.sendall(b"ENDHDR\n")

    def _read_headers(self, conn):
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

    def _recv_exact(self, conn, size):
        data = b""
        while len(data) < size:
            chunk = conn.recv(size - len(data))
            if not chunk:
                raise ConnectionError("Desconectado durante download")
            data += chunk
        return data

    def _checksum_buf(self, data):
        h = hashlib.sha256()
        h.update(data)
        return h.hexdigest()

    def pull(self, *filenames, folder="Docs", outdir="."):
        if not filenames:
            print("Nenhum arquivo especificado para pull.")
            return

        conn = self._connect()

        init_hdr = {
            "CMD": "pull",
            "COUNT": str(len(filenames)),
            "DIR": folder
        }
        self._send_headers(conn, init_hdr)

        for name in filenames:
            self._send_headers(conn, {"NAME": name})

        for name in filenames:
            hdr = self._read_headers(conn)

            if hdr.get("STATUS") != "ok":
                print(f"erro ao puxar {name}: {hdr}")
                continue

            size = int(hdr["SIZE"])
            expected_checksum = hdr.get("CHECK")
            actual_name = hdr["NAME"]

            payload = self._recv_exact(conn, size)
            actual_checksum = self._checksum_buf(payload)

            if expected_checksum != actual_checksum:
                print(f"checksum incorreto para {actual_name}")
            else:
                print(f"checksum OK: {actual_name}")

            out_path = os.path.join(outdir, actual_name)
            os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(payload)

            print(f"salvo: {out_path}")

        conn.close()

if __name__ == "__main__":
    import sys
    from pathlib import Path
    from dotenv import load_dotenv

    env_path = Path.home() / "myfileserverconfigs" / ".env"
    load_dotenv(env_path)

    server_ip = os.getenv("server_ip")
    if not server_ip:
        print("server_ip não configurado no .env")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Uso: filepull arquivo1 arquivo2 ...")
        sys.exit(1)

    puller = FilePuller(server_ip, 6000)
    puller.pull(*sys.argv[1:])


