from socket import socket
from subprocess import Popen, CREATE_NEW_CONSOLE
import requests
import matplotlib.pyplot as plt
import networkx as nx
from json import loads


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


class Manager:
    @staticmethod
    def find_free_port():
        s = socket()
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    def __init__(self):
        self.processes = []

    def run(self, num):
        for i in range(num):
            port = self.find_free_port()
            proc = Process(port)
            self.processes.append(proc)

    def stop(self):
        for proc in self.processes:
            proc.kill()
        self.processes = []

    def mine(self):
        for proc in self.processes:
            proc.send('/mine')

    def register_all(self):
        for x in self.processes:
            for y in self.processes:
                if x.pid != y.pid:
                    x.send(f"/register/{y.port}")

    def kgraph(self):
        # knowledge graph
        G = nx.DiGraph()
        for x in self.processes:
            resp = x.send("/nodes")
            resp = loads(resp.text)
            for n in resp:
                G.add_edge(x.port, int(n))
            if not resp:
                G.add_node(x.port)
        nx.draw(G, with_labels=True)
        plt.show()


class Parser:
    def __init__(self):
        pass

    def loop(self):
        while True:
            cmd = input()
            if not cmd: continue
            self.parse(cmd)

    def parse(self, cmd):
        cmd = [a.strip() for a in cmd.split()]
        naem = cmd[0]
