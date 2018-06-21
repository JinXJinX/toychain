# coding=utf-8
import time
import json
import hashlib
import uuid
from random import randint

import requests
import config


class ToyChain:
    def __init__(self, pvt_key=None):
        self.tx_pool = []
        self.nodes = get_nodes()
        self.pvt_key = pvt_key or str(uuid.uuid4()).replace('-', '')
        self.pub_key = 'asd'  # TODO generate pub key from pvt key
        self.chain = self._get_chain_from_node()

    def _get_chain_from_node(self):
        if self.nodes:
            return get_chain(self.nodes[0])
        else:
            # Create the genesis block
            print('mining first block')
            block = genesis_block(self.pub_key)
            return [block]


def hash(inp):
    """
    Creates a SHA-256 hash of a input dictionary

    :param inp: a dict, such as block, tx
    """
    s = json.dumps(inp, sort_keys=True).encode()
    return hashlib.sha256(s).hexdigest()


def get_nonce(header, target):
    while True:
        header = dict(header)
        nonce = randint(0, 10000)  # TODO reset max range
        header['nonce'] = nonce
        header_string = json.dumps(header, sort_keys=True).encode()
        hash = hashlib.sha256(header_string).hexdigest()
        if hash < target:
            return nonce
        time.sleep(1)  # 1 second


def _get(**kwargs):
    try:
        r = requests.get(**kwargs, timeout=5)
        if r.status_code == 200:
            return True, r.json()
    except requests.exceptions.ConnectTimeout as e:
        print(e)
    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.ReadTimeout as e:
        print(e)
    return False, None


def _post(**kwwargs):
    pass


def get_chain(node):
    chain = []
    height = 1
    while True:
        ret, data = _get(url=f'http://{node}/get_block/{height}')
        if ret and data['ok']:
            chain.append(data['block'])
            height += 1
        else:
            break
    return chain


def get_nodes():
    nodes = set()
    for node in config.DEFAULT_NODES:
        ret, _ = _get(url=f'http://{node}/ping')
        if ret:
            nodes.add(node)
    return list(nodes)


def verify_chain():
    pass


def verify_tx():
    pass


def verify_block():
    pass


def resolve_conflicts():
    pass


def post_data(type, data):
    postfix = f'/add_{type}'
    for node in nodes:
        r = requests.post(url, data)


def post_tx(tx):
    return post_data('tx', tx)


def post_block(block):
    return post_data('block', block)


def post_node(node):
    return post_data('node', node)


def genesis_block(pub_key):
    header = {
        'idx': 1,
        'ts': time.time(),
        'prev_hash': '',
    }
    coinbase_tx = new_tx('0', pub_key, 50)
    txs = [coinbase_tx]

    block = dict(header)
    target = config.TARGET
    nonce = get_nonce(header, target)  # use default target
    block['nonce'] = nonce
    block['tx'] = txs
    block['hash'] = ''  # TODO caculate block hash
    return block


def new_block(toychain):
    header = {
        'idx': len(toychain.chain) + 1,
        'ts': time.time(),
        'prev_hash': toychain.chain[-1]['hash'],
    }
    coinbase_tx = new_tx('0', toychain.pub_key, 50)
    txs = [coinbase_tx] + toychain.tx_pool
    # Reset the current list of transactions
    toychain.tx_pool = []

    block = dict(header)
    nonce = get_nonce(header, config.TARGET)
    block['nonce'] = nonce
    block['tx'] = txs
    block['hash'] = ''  # TODO caculate block hash
    toychain.chain.append(block)


def new_tx(sender, recipient, amount):
    tx = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount,
        'ts': time.time(),
    }
    return tx
