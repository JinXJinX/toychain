# coding=utf-8
import json
from urllib.parse import urlparse


from flask import Flask, jsonify, request
import toychain
from miner import Miner
import config

app = Flask(__name__)
tc = toychain.ToyChain()
miner = Miner(tc)

if config.MINING:
    miner.start()


@app.route('/add_node', methods=['POST'])
def add_node():
    """
    Receive new node, add it to register node list, and broadcast it
    """
    ip = request.remote_addr
    port = request.environ.get('REMOTE_PORT')
    if ip not in tc.get_nodes():
        # TODO broadcast to other node
        tc.add_node(f'{ip}:{port}')
        return jsonify({'ok': True}), 200
    return jsonify({'ok': False}), 200


@app.route('/add_tx', methods=['POST'])
def add_tx():
    """
    Receive new tx, verify it then broadcast it
    """
    data = request.get_json()
    tx = json.loads(data.get('tx'))
    pass


@app.route('/add_block', methods=['POST'])
def add_block():
    """
    Receive new block, verify it then add it to chain and broadcast it
    """
    data = request.get_json()
    block = json.loads(data.get('block'))
    tc.add_block(block)
    # TODO if mining, stop the mining thread
    return jsonify({'ok': True}), 200


@app.route('/get_block/<int:height>', methods=['GET'])
def get_block(height):
    """
    Get block by height/idx
    """
    chain = tc.get_chain()
    if height >= len(chain):
        return jsonify({'ok': False}), 200
    response = {
        'ok': True,
        'block': chain[height]
    }
    return jsonify(response), 200


@app.route('/get_last_block', methods=['GET'])
def get_last_block():
    """
    Get the lastest block in the chain
    """
    chain = tc.get_chain()
    response = {
        'ok': True,
        'block': chain[-1],
        'height': len(chain),
    }
    return jsonify(response), 200


@app.route('/get_node', methods=['GET'])
def get_node():
    """
    Get a list of registered nodes
    """
    response = {
        'ok': True,
        'nodes': tc.get_nodes()
    }
    return jsonify(response), 200


@app.route('/ping', methods=['GET'])
def ping():
    """
    ping
    """
    return jsonify({'ok': True}), 200
