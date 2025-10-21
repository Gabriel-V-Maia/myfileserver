import sys
from send import FileClient

if len(sys.argv) < 2:
    print("uso: push <arquivo1> <arquivo2> ...")
    sys.exit(1)

files = sys.argv[1:]
client = FileClient(host="127.0.0.1", port=6000)
client.push(*files)
