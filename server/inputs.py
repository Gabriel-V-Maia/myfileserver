from utils.py import Logger


class InputManagement(self):
    def __init__(self, name):
        self.name = name
        self.running = False

    def start(self):
        logger = Logger("[InputManagement]")
        self.running = True

        logger.info("Starting input management service")

        while self.running:
            cmd = input()



