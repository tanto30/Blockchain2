from uuid import uuid4
from sys import argv
from Node.blockchain import Chain
from flask import Flask, render_template


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
    chain.new_block()
    return chain.to_json(), 200, content_type


@app.route('/transaction/<to>/<amount>')
def transaction(to, amount):
    chain.new_transaction(to, amount)


#### UI ####

@app.route('/ui')
def ui():
    return render_template("hello.html", data=chain.to_json())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1222)
