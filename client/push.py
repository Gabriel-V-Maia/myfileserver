import sys
from send import FileClient
from dotenv import load_dotenv
import os 
from pathlib import Path

load_dotenv(Path.home() / 'myfileserverconfig' / '.env')

server_ip = os.getenv("server_ip")

if not server_ip:
    print("server_ip não configurado, abortando")
    sys.exit(1)

if len(sys.argv) < 2:
    print("uso: push <arquivo1> <arquivo2> ...")
    sys.exit(1)

files = sys.argv[1:]
client = FileClient(host=server_ip, port=6000)
client.push(*files)

