import ctypes

from utils import Logger
from server import FileServer

def ensure_admin():
    if os.name == "nt":   
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            is_admin = False
        if not is_admin:
            params = " ".join([f'"{arg}"' for arg in sys.argv])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
            sys.exit()
    else:  
        if os.geteuid() != 0:
            print("[!] este script precisa ser rodado como root")
            os.execvp("sudo", ["sudo", sys.executable] + sys.argv)

       
if __name__ == "__main__":
    ensure_admin()  
    fileserver = fileServer()
    fileserver.start()
