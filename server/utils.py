from colorama import init, Back, Style

init(autoreset=True)

class Logger:
    def __init__(self, name, displayName=False) -> None:
        self.name = name 
        self.display = displayName

    def warn(self, text):
        if self.display:
             print(f"{Back.YELLOW} [{self.name}] [!] {text}") 
        else:
             print(f"{Back.YELLOW} [!] {text}")
        
    def info(self, text):
         if self.display:
             print(f"{Back.BLUE} [{self.name}] {text}") 
         else:
             print(f"{Back.BLUE} {text}")
         
    def error(self, text):
         if self.display:
             print(f"{Back.RED} [{self.name}] [ERROR] {text}") 
         else:
             print(f"{Back.RED} [ERROR] {text}")
         
