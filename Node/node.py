from uuid import uuid4
from Node.blockchain import Chain
from flask import Flask, render_template
import matplotlib.pyplot as plt
import networkx as nx
from Node.jsonaux import jsonify

content_type = {'Content-Type': 'Application/json'}

app = Flask(__name__)

#### API ####

@app.route('/')
def main():
    return jsonify(chain), 200, content_type


@app.route('/mine')
def mine():
    chain.mine()
    return jsonify(chain), 200, content_type

@app.route('/transaction/<to>/<amount>')
def transaction(to, amount):
    chain.transaction(to, amount)
    return jsonify(chain), 200, content_type


@app.route('/resolve')
def resolve():
    chain.resolve()
    return jsonify(chain), 200, content_type


@app.route('/register/<id>')
def register(id):
    chain.register(id)
    return jsonify(chain), 200, content_type

#### UI ####

@app.route('/ui')
def ui():
    return render_template("hello.html", data=jsonify(chain))


@app.route('/graph')
def graph():
    G = chain.chain.transaction_graph()
    nx.draw(G, with_labels=True)
    plt.savefig("static/img.png")
    plt.close()
    return render_template("image.html")


@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    return response

if __name__ == '__main__':
    port = int(input())
    chain = Chain(port)
    app.run(host='0.0.0.0', port=port)
