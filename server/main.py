import ctypes

import os
from utils import Logger
from inputs import InputManagement

def ensure_admin():
    if os.name == "nt":   
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            is_admin = False
        if not is_admin:
            print("[!] Rode esse script como administrador")
            sys.exit()
    else:  
        if os.geteuid() != 0:
            print("[!] este script precisa ser rodado como root")
            break
       
if __name__ == "__main__":
    ensure_admin()  
    inputss = InputManagement("Input Manager")
    inputss.start()
