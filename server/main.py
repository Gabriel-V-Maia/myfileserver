import socket
import os
from pathlib import Path

class fileServer:
    def __init__(self, HOST="127.0.0.1", PORT=6000,STORAGE_DIR="./storage"):
        fileServer.HOST = HOST 
        fileServer.PORT = PORT
        self.STORAGE_DIR = Path(STORAGE_DIR)
        self.STORAGE_DIR.mkdir(exist_ok=True)
    
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))
            s.listen()

            print(f"[+] servidor iniciado")
            print(f"[i] diretório de storage: {self.STORAGE_DIR}")
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"[*] cliente conectado: {addr}")
                    self.handle(conn, addr)


    def handle(self, conn: socket, addr: tuple):
        try: 
            data = conn.recv(1024)
            cmd = data.decode().strip()

            match cmd.split()[0]:
                case 'push':
                    self._push(conn, cmd)
                case 'pull':
                    self._pull(conn, cmd)

                
        except Exception as e:
            print(f"{e}")

    def _push(self, conn: socket, cmd):
        """Recebe arquivos do client"""

        try:
            args = cmd.split(' ')
            files = args[1:]

            if not files:
                conn.sendall(b"nenhum arquivo especificado")
                return -1
            
            for file in files:
                if ".." in file or "/" in file or "\\" in file:
                    conn.sendall(f"nome de arquivo inválido: {file}".encode())
                    return
                
                filepath = self.STORAGE_DIR / file
                conn.sendall(b"OK")  
                
                filesize_str = conn.recv(1024).decode().strip()
                filesize = int(filesize_str)
                
                conn.sendall(b"OK")  
                
                received = 0
                with open(filepath, "wb") as f:
                    while received < filesize:
                        chunk = conn.recv(min(4096, filesize - received))
                        if not chunk:
                            break
                        f.write(chunk)
                        received += len(chunk)
                
                print(f"arquivo armazenado: {file}")
            
            conn.sendall(b"OK")
        except Exception as e:
            print(f"{e}")

    def _pull(self, conn, cmd):
        try:
            args = cmd.split()
            items = args[1:] 
            
            if not items:
                conn.sendall(b"nenhum item especificado")
                return
            
            for item in items:
                path = self.STORAGE_DIR / item
                
                if not path.exists():
                    conn.sendall(f"{item} não encontrado".encode())
                    return
                
                if path.is_file():
                    self._send_file(conn, path, item)
                
                elif path.is_dir():
                    for file in path.rglob("*"):  
                        if file.is_file():
                            relative_path = file.relative_to(self.STORAGE_DIR)
                            self._send_file(conn, file, str(relative_path))
        
        except Exception as e:
            conn.sendall(f"ERRO: {e}".encode())

    def _send_file(self, conn, filepath, filename):
        """Helper pra enviar um arquivo"""
        filesize = filepath.stat().st_size
        conn.sendall(str(filesize).encode())
        conn.recv(1024)  # confirmação
        
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                conn.sendall(chunk)
    
        print(f"arquivo enviado: {filename}")
        
        
        
if __name__ == "__main__":
    fileserver = fileServer()
    fileserver.start()
