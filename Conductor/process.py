from subprocess import Popen, CREATE_NEW_CONSOLE
import requests
import sys
from os import chdir, path

class Process(Popen):
    def __init__(self, port):
        is_exe = getattr(sys, 'frozen', False)
        cmd = "python ../Node " if not is_exe else "app.exe "
        if is_exe:
            chdir(path.dirname(sys.executable))
        super().__init__(cmd + str(port), creationflags=CREATE_NEW_CONSOLE)
        self.port = port
        print(f"Started node instance with PID {self.pid} on Port {port}")
        self.address = f"http://127.0.0.1:{port}"

    def send(self, ep):
        resp = requests.get(self.address + ep)
        print(f"PID:{self.pid}, PORT:{self.port} - {resp.status_code}")
        return resp
