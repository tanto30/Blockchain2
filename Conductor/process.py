from subprocess import Popen, CREATE_NEW_CONSOLE
import requests


class Process(Popen):
    def __init__(self, port):
        super().__init__("python ../Node " + str(port), creationflags=CREATE_NEW_CONSOLE)
        self.port = port
        print(f"Started node instance with PID {self.pid} on Port {port}")
        self.address = f"http://127.0.0.1:{port}"

    def send(self, ep):
        resp = requests.get(self.address + ep)
        print(f"PID:{self.pid}, PORT:{self.port} - {resp.status_code}")
        return resp
