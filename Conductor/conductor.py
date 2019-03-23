from socket import socket
from subprocess import Popen, CREATE_NEW_CONSOLE
import requests
import matplotlib.pyplot as plt
import networkx as nx
from json import loads

def find_free_port():
    s = socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

processes = []


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

while (True):
    cmd = input()
    cmd = [a.strip() for a in cmd.split()]
    if not cmd:
        continue
    if cmd[0] == "run":
        num = int(cmd[1])
        for i in range(num):
            port = find_free_port()
            proc = Process(port)
            processes.append(proc)
    elif cmd[0] == "stop":
        for process in processes:
            process.kill()
        processes = []
    elif cmd[0] == "mine":
        for process in processes:
            process.send("/mine")
    elif cmd[0] == "register_all":
        for x in processes:
            for y in processes:
                if x.pid != y.pid:
                    x.send(f"/register/{y.port}")
    elif cmd[0] == "knowledge_graph":
        G = nx.DiGraph()
        for x in processes:
            resp = x.send("/nodes")
            resp = loads(resp.text)
            for n in resp:
                G.add_edge(x.port, int(n))
            if not resp:
                G.add_node(x.port)
        nx.draw(G, with_labels=True)
        plt.show()
