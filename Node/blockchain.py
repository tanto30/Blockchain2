from time import time
from hashlib import sha256
import networkx as nx
import requests
from Node.jsonaux import jsonify
from json import loads


class Block:
    def __init__(self, index, constraint, transactions):
        self.index = index
        self.constraint = constraint
        self.transactions = transactions
        self.timestamp = time()
        self.__mine()

    def __repr__(self):
        return jsonify(self)

    @staticmethod
    def from_json(json):
        res = Block(0, 0, [])
        res.__dict__ = loads(json)
        return res

    def hash(self):
        return sha256(jsonify(self).encode()).hexdigest()

    def __mine(self):
        self.pow = 0
        while self.validate() is False:
            self.pow += 1

    def validate(self):
        return self.hash().endswith("00")


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount


class Chain:
    def __init__(self, port):
        self.port = port
        self.nodes = set()
        self.chain = [Block(0, "Genesis", [])]
        self.payments = []

    def __repr__(self):
        return str(self.chain)

    def __len__(self):
        return len(self.chain)

    def to_json(self):
        return jsonify(self)

    @staticmethod
    def __from_json(json):
        res = Chain(0)
        res.__dict__ = loads(json)
        for i in range(len(res)):
            tmp = res.chain[i]
            res.chain[i] = Block(0, 0, [])
            res.chain[i].__dict__ = tmp
        return res

    def mine(self):
        self.transaction(self.port, 1)
        self.chain.append(
            Block(
                len(self.chain),
                self.chain[-1].hash(),
                self.payments[:]
            )
        )
        self.payments = []

    def transaction(self, receiver, amount):
        self.payments.append(
            Transaction(
                self.port,
                receiver,
                amount
            )
        )

    def register(self, port):
        self.nodes.add(port)

    def resolve(self):
        nodes = self.__all_nodes()
        max_len = len(self.chain)
        new_chain = None
        for node in nodes:
            length = len(node)
            if length > max_len and self.__validate(node):
                max_len = length
                new_chain = node.chain
        if new_chain:
            self.chain = new_chain
            return True
        return False

    def transaction_graph(self):
        G = nx.DiGraph()
        for block in self.chain:
            for trans in block.transactions:
                G.add_edge(trans.sender, trans.receiver)
        for trans in self.payments:
            G.add_edge(str(trans.sender), trans.receiver)
        return G

    def __validate(self, chain):
        return all(
            [b.validate() for b in chain.chain]
        )

    def __all_nodes(self):
        res = []
        for port in self.nodes:
            res.append(Chain.__from_json(requests.get("http://127.0.0.1:" + port).text))
        return res


if __name__ == '__main__':
    c1 = Chain(1)
    for i in range(10):
        c1.mine()
    a = c1.to_json()
    c2 = Chain.__from_json(a)
    b = c2.to_json()
    assert a == b
