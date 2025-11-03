from pathlib import Path
import os 
import socket

from utils import Logger 

logger = Logger("[File Operations]")

class ServerOperations:
    def _push(self, conn: socket, cmd):
        try:
            args = cmd.split(' ')
            files = args[1:]

            if not files:
                conn.sendall(b"nenhum arquivo especificado")
                return
            
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
                
                print(f"[+] arquivo armazenado: {file}")
            
            conn.sendall(b"OK")
        except Exception as e:
            logger.error(f"[!] erro em _push: {e}")
            conn.sendall(f"ERRO: {e}".encode())

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
            logger.error(f"[!] erro em _pull: {e}")
            conn.sendall(f"ERRO: {e}".encode())

    def _send_file(self, conn, filepath, filename):
        filesize = filepath.stat().st_size
        conn.sendall(str(filesize).encode())
        conn.recv(1024)
        
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                conn.sendall(chunk)
    
        logger.info(f"[+] arquivo enviado: {filename}")


