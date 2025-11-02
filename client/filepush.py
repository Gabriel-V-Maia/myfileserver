import sys
from filesend import FileClient
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path.home() / 'myfileserverconfigs' / '.env'
load_dotenv(dotenv_path=env_path)

server_ip = os.getenv("server_ip")
if not server_ip:
    print(f"server_ip não configurado no {env_path}, abortando")
    sys.exit(1)

if len(sys.argv) < 2:
    print("uso: push <arquivo1> <arquivo2> ...")
    sys.exit(1)

files = sys.argv[1:]
client = FileClient(host=server_ip, port=6000)
client.push(*files)

