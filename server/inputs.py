from utils import Logger
from server import FileServer

from pathlib import Path
import threading

class Commands:
    def __init__(self):
        self.logger = Logger("[Commands]")

        self.map = {
            "devices": self.get_devices,
        }

        self.fs = None

    # ----------------------------------------
    # START FILESERVER
    # ----------------------------------------

    def fileserver(self, host=None, port=None, storagedir=None):

        if host is None and port is None and storagedir is None:
            self.fs = FileServer()
        else:

            if port is not None:
                port = int(port)

            self.fs = FileServer(
                host or "0.0.0.0",
                port or 6000,
                storagedir or str(Path.home() / "fileserver")
            )

        t = threading.Thread(target=self.fs.start, daemon=True)
        t.start()
        self.logger.info("FileServer started")

    # ----------------------------------------
    # GET DEVICES
    # ----------------------------------------
    
    def get_devices(self):
        if not self.fs:
            print("FileServer is not running.")
            return

        conns = self.fs.get_active_connections()

        for a, b in conns.items():
            print(a, "-", b)

    # ----------------------------------------
    # GET COMMAND PARSER
    # ----------------------------------------
    
    def get(self, args):
        if not args:
            print("get command received no args")
            return

        part1 = args[0]

        matches = [name for name in self.map if name.startswith(part1)]

        if not matches:
            print("unknown get option")
            return

        if len(matches) > 1:
            print(f"ambiguous get option: {matches}")
            return

        func = self.map[matches[0]]
        func()

    # ----------------------------------------
    # MAIN EXECUTOR
    # ----------------------------------------
    
    def execute(self, cmd):
        parts = cmd.split()
        if not parts:
            return None

        name = parts[0]
        args = parts[1:]

        if hasattr(self, name):
            method = getattr(self, name)
            return method(*args)
        
        print(f"Unknown command: {name}")
        return None


class InputManagement:
    def __init__(self, name):
        self.name = name
        self.running = False
        self.logger = Logger("[InputManagement]")
        self.commands = Commands()

    def start(self):
        self.running = True
        self.logger.info("Starting input management service")

        while self.running:
            cmd = input("> ")
            if cmd == "exit":
                self.running = False
                self.logger.error("Stopping input management service")
                break

            self.commands.execute(cmd)

