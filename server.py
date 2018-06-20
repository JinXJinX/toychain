# coding=utf-8
import json

from flask import Flask, jsonify, request
import toychain

app = Flask(__name__)
tc = toychain.ToyChain()


@app.route('/add_node', methods=['POST'])
def add_node():
    """
    Receive new node, add it to register node list, and broadcast it
    """
    pass


@app.route('/add_tx', methods=['POST'])
def add_tx():
    """
    Receive new tx, verify it then broadcast it
    """
    pass


@app.route('/add_block', methods=['POST'])
def add_block():
    """
    Receive new block, verify it then add it to chain and broadcast it
    """
    pass


@app.route('/get_block', methods=['GET'])
def get_block():
    """
    Get block by height/idx
    """
    pass


@app.route('/get_last_block', methods=['GET'])
def get_last_block():
    """
    Get the lastest block in the chain
    """
    response = {
        "block": tc.chain[-1]
    }
    return jsonify(response), 200


@app.route('/get_node', methods=['GET'])
def get_node():
    """
    Get a list of registered nodes
    """
    pass
