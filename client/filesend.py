import socket
import os
import hashlib

class FileSender:
    def __init__(self, host="127.0.0.1", port=6000):
        self.host = host
        self.port = port

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
        buf = ""
        while True:
            chunk = conn.recv(1024).decode()
            if not chunk:
                raise ConnectionError("Conexao perdida")

            buf += chunk
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                line = line.strip()

                if line == "ENDHDR":
                    return headers
                if "=" in line:
                    k, v = line.split("=", 1)
                    headers[k] = v

    def _checksum(self, path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()

    def push(self, *filepaths, folder="Docs"):
        valid_files = []

        for fp in filepaths:
            if not os.path.exists(fp):
                print(f"Arquivo nao encontrado: {fp}")
                continue
            valid_files.append(fp)

        if not valid_files:
            print("Nenhum arquivo valido para enviar.")
            return

        conn = self._connect()

        # ---- header inicial da operação ----
        global_hdr = {
            "CMD": "push",
            "COUNT": str(len(valid_files)),
            "DIR": folder
        }
        self._send_headers(conn, global_hdr)

        for path in valid_files:
            name = os.path.basename(path)
            size = os.path.getsize(path)
            cksum = self._checksum(path)

            fhdr = {
                "NAME": name,
                "SIZE": str(size),
                "CHECK": cksum
            }
            self._send_headers(conn, fhdr)

            # payload
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    conn.sendall(chunk)

            ack = self._read_headers(conn)
            if ack.get("STATUS") != "ok":
                print(f"falhou {name}:", ack)
            else:
                print(f"enviado {name} (OK)")

        conn.close()

if __name__ == "__main__":
    import sys
    from pathlib import Path
    from dotenv import load_dotenv

    env = Path.home() / "myfileserverconfigs" / ".env"
    load_dotenv(env)

    ip = os.getenv("server_ip")
    if not ip:
        print("server_ip não configurado no .env")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Uso: filesend arquivo1 arquivo2 ...")
        sys.exit(1)

    sender = FileSender(ip, 6000)
    sender.push(*sys.argv[1:])

