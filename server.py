# coding=utf-8
from urllib.parse import urlparse


from flask import Flask, jsonify, request
import toychain
from miner import Miner
import settings

app = Flask(__name__)

tc = None
miner = None


def init():
    global tc
    global miner

    pvt_key = app.config.get('PVT_KEY')
    tc = toychain.ToyChain(app.config['PORT'], pvt_key=pvt_key)

    if not pvt_key:
        filename = app.config['CONFIG_FILENAME']
        with open(f'{filename}.py', 'a') as f:
            f.write(f'PVT_KEY = \'\'\'{tc.get_pvt_key()}\'\'\'')

    print(tc.get_address())
    if app.config['MINING']:
        miner = Miner(tc)
        miner.start()


@app.route('/add_node', methods=['POST'])
def add_node():
    """
    Receive new node, add it to register node list, and broadcast it
    """
    ip = request.remote_addr
    data = request.get_json() or {}
    port = data.get('node', {}).get('port')
    if not port:
        return jsonify({'ok': False}), 200

    node = f'{ip}:{port}'
    rst = tc.add_node(node)
    return jsonify({'ok': rst}), 200


@app.route('/add_tx', methods=['POST'])
def add_tx():
    """
    Receive new tx, verify it then broadcast it
    """
    data = request.get_json() or {}
    tx = data.get('tx')
    rst = tc.add_tx(tx)
    return jsonify({'ok': rst}), 200


@app.route('/add_block', methods=['POST'])
def add_block():
    """
    Receive new block, verify it then add it to chain and broadcast it
    """
    data = request.get_json() or {}
    block = data.get('block')
    if not block:
        return jsonify({'ok': False}), 200

    rst = tc.add_block(block)
    # TODO if mining, stop the mining thread
    return jsonify({'ok': rst}), 200


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
        'height': len(chain)-1,
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


@app.route('/get_ledger', methods=['GET'])
def get_ledger():
    """
    Get a list of ledger
    """
    response = {
        'ok': True,
        'ledger': tc.get_ledger()
    }
    return jsonify(response), 200


@app.route('/ping', methods=['GET'])
def ping():
    """
    ping
    """
    return jsonify({'ok': True}), 200


# WARNING this url for test only
@app.route('/send_coin', methods=['POST'])
def send_coin():
    """

    """
    data = request.get_json() or {}
    address = data.get('address')
    amount = data.get('amount')
    fee = data.get('fee')
    if None in (address, amount, fee):
        return jsonify({'ok': False}), 200
    rst = tc.send_coin(address, amount, fee)
    return jsonify({'ok': rst}), 200
