import socket
import os
from pathlib import Path
import sys
import ctypes
from operations import ServerOperations  

from utils import Logger
logger = Logger("[Server]")

def ensure_admin():
    if os.name == "nt":   
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            is_admin = False
        if not is_admin:
            params = " ".join([f'"{arg}"' for arg in sys.argv])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
            sys.exit()
    else:  
        if os.geteuid() != 0:
            print("[!] este script precisa ser rodado como root")
            os.execvp("sudo", ["sudo", sys.executable] + sys.argv)

class fileServer(ServerOperations):  
    def __init__(self, HOST="0.0.0.0", PORT=6000, STORAGEDIR=str(Path.home() / "fileserver")):
        self.HOST = HOST 
        self.PORT = PORT
        self.STORAGE_DIR = Path(STORAGEDIR)
        self.STORAGE_DIR.mkdir(exist_ok=True)
    
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))
            s.listen()
            logger.info(f"[+] servidor iniciado em {self.HOST}:{self.PORT}")
            logger.info(f"[i] diretório de storage: {self.STORAGE_DIR}")
            
            while True:
                conn, addr = s.accept()
                with conn:
                    logger.warn(f"[*] cliente conectado: {addr}")
                    self.handle(conn, addr)
    
    def handle(self, conn: socket, addr: tuple):
        try: 
            data = conn.recv(1024)
            cmd = data.decode().strip()
            
            if not cmd:
                return
                
            cmd_type = cmd.split()[0]
            
            match cmd_type:
                case 'push':
                    self._push(conn, cmd)
                case 'pull':
                    self._pull(conn, cmd)
                case _:
                    conn.sendall(b"comando invalido")
                
        except Exception as e:
            logger.error(f"[!] erro ao processar comando: {e}")
        
if __name__ == "__main__":
    ensure_admin()  
    fileserver = fileServer()
    fileserver.start()
