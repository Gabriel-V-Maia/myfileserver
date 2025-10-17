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

            match cmd:
                case 'push':
                    pass
                case 'pull':
                    pass
                
        except Exception as e:
            print(f"{e}")
            
        

