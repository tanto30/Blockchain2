from socket import socket
from subprocess import Popen, CREATE_NEW_CONSOLE
import requests
import matplotlib.pyplot as plt
import networkx as nx
from json import loads

def find_free_port():
    s = socket()
    s.bind(('', 0))
    return s.getsockname()[1]


processes = []

while (True):
    cmd = input()
    cmd = [a.strip() for a in cmd.split()]
    if not cmd:
        continue
    if cmd[0] == "run":
        num = int(cmd[1])
        for i in range(num):
            port = find_free_port()
            proc = Popen("python ../Node " + str(port), creationflags=CREATE_NEW_CONSOLE)
            proc.port = port
            processes.append(proc)
            print(f"Started node instance with PID {proc.pid} on Port {port}")
    elif cmd[0] == "stop":
        for process in processes:
            process.kill()
        processes = []
    elif cmd[0] == "mine":
        for process in processes:
            resp = requests.get("http://127.0.0.1:" + str(process.port) + "/mine")
            print(f"PID:{process.pid},PORT:{process.port} - {resp.status_code}")
    elif cmd[0] == "register_all":
        for x in processes:
            for y in processes:
                if x.pid != y.pid:
                    resp = requests.get(f"http://127.0.0.1:{x.port}/register/{y.port}")
                    print(f"PID:{x.pid},PORT:{x.port} - {resp.status_code}")
    elif cmd[0] == "knowledge_graph":
        G = nx.DiGraph()
        for x in processes:
            resp = requests.get(f"http://127.0.0.1:{x.port}/nodes")
            print(f"PID:{x.pid},PORT:{x.port} - {resp.status_code}")
            resp = loads(resp.text)
            for n in resp:
                G.add_edge(x.port, int(n))
            if not resp:
                G.add_node(x.port)
        nx.draw(G, with_labels=True)
        plt.show()
