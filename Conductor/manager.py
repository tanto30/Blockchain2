from socket import socket
import matplotlib.pyplot as plt
import networkx as nx
from json import loads
from process import Process

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

    def mine_one(self):
        if self.processes:
            self.processes[0].send("/mine")

    def resolve(self):
        for x in self.processes:
            x.send("/resolve")
