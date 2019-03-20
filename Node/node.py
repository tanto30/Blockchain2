from uuid import uuid4
from Node.blockchain import Chain
from flask import Flask, render_template
import matplotlib.pyplot as plt
import networkx as nx
class Node:
    def __init__(self):
        chain = Chain(int(uuid4()))


app = Flask(__name__)
chain = Chain(int(uuid4()))

content_type = {'Content-Type': 'Application/json'}


#### API ####

@app.route('/')
def main():
    return chain.to_json(), 200, content_type


@app.route('/mine')
def mine():
    chain.mine()
    return chain.to_json(), 200, content_type


@app.route('/transaction/<to>/<amount>')
def transaction(to, amount):
    chain.new_transaction(to, amount)
    return chain.to_json(), 200, content_type

#### UI ####

@app.route('/ui')
def ui():
    return render_template("hello.html", data=chain.to_json())


@app.route('/graph')
def graph():
    G = chain.transaction_graph()
    print(G.graph)
    nx.draw(G)
    plt.savefig("static/img.png")
    return render_template("image.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1222)
