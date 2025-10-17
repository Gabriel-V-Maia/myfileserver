import socket
import os
import sys
from pathlib import Path

class FileClient:
    def __init__(self, host="127.0.0.1", port=6000):
        self.host = host
        self.port = port
    
    def connect(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def push(self, *filenames):
        try:
            s = self.connect()
            s.connect((self.host, self.port))
            
            cmd = f"push {' '.join(filenames)}"
            s.sendall(cmd.encode())
            
            for filename in filenames:
                if not os.path.exists(filename):
                    print(f"erro: {filename} não encontrado")
                    continue
                
                resp = s.recv(1024).decode()
                if resp != "OK":
                    print(f"erro ao enviar {filename}: {resp}")
                    continue
                
                filesize = os.path.getsize(filename)
                s.sendall(str(filesize).encode())
                
                resp = s.recv(1024).decode()
                
                with open(filename, "rb") as f:
                    while True:
                        chunk = f.read(4096)
                        if not chunk:
                            break
                        s.sendall(chunk)
                
                print(f"Enviado: {filename}")
            
            resp = s.recv(1024).decode()
            s.close()
        
        except Exception as e:
            print(f"Erro: {e}")
    
    def pull(self, *filenames):
        try:
            s = self.connect()
            s.connect((self.host, self.port))
            
            cmd = f"pull {' '.join(filenames)}"
            s.sendall(cmd.encode())
            
            for filename in filenames:
                resp = s.recv(1024).decode()
                
                if resp.startswith("ERRO"):
                    print(f"Erro: {resp}")
                    continue
                
                filesize = int(resp)
                s.sendall(b"OK")
                
                os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
                
                received = 0
                with open(filename, "wb") as f:
                    while received < filesize:
                        chunk = s.recv(min(4096, filesize - received))
                        if not chunk:
                            break
                        f.write(chunk)
                        received += len(chunk)
                
                print(f"Baixado: {filename}")
            
            s.close()
        
        except Exception as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python client.py push <arquivo1> <arquivo2> ...")
        print("  python client.py pull <arquivo1> <arquivo2> ...")
        sys.exit(1)
    
    cmd = sys.argv[1]
    files = sys.argv[2:]
    
    client = FileClient(host="127.0.0.1", port=6000)
    
    if cmd == "push":
        client.push(*files)
    elif cmd == "pull":
        client.pull(*files)
    else:
        print(f"Comando desconhecido: {cmd}")