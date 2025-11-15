from utils import Logger
from server import FileServer


"""
    def __init__(self, HOST="0.0.0.0", PORT=6000, STORAGEDIR=str(Path.home() / "fileserver")):
        self.HOST = HOST 
        self.PORT = PORT
        self.STORAGE_DIR = Path(STORAGEDIR)
        self.STORAGE_DIR.mkdir(exist_ok=True)
""" 

class Commands:
    def __init__(self):
        self.logger = Logger("[Commands]")

    def fileserver(self, host, port, storagedir):
        self.fs = FileServer(str(host), port, storagedir)
        self.fs.start()

    def get_devices(self):
        for key, value in self.fs.get_active_connections().items():
            print(conns[key], " - ", conns[value])

    def execute(self, cmd):
        parts = cmd.split()
        if not parts:
            return None
        name = parts[0]
        args = parts[1:]
        if hasattr(self, name):
            return getattr(self, name)(*args) if args else getattr(self, name)()
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

