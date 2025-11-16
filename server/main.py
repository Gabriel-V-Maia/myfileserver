import ctypes

import os
from utils import Logger
from inputs import InputManagement

logger = Logger("Main.py")

def ensure_admin():
    if os.name == "nt":   
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            is_admin = False
        if not is_admin:
            print("[!] é recomendado que rode esse script como administrador")
    else:  
        if os.geteuid() != 0:
            logger.warn("[!] é recomendado que este script seja rodado como root")

if __name__ == "__main__":
    ensure_admin()  
    inputss = InputManagement("Input Manager")
    inputss.start()
