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
        self.chain = get_chain_from_node(self.nodes, self.pub_key)
        print(self.nodes)

    def new_block(self):
        chain = self.chain
        header = {
            'idx': len(chain) + 1,
            'ts': time.time(),
            'prev_hash': chain[-1]['hash'],
        }
        coinbase_tx = new_tx('0', self.pub_key, 50)
        txs = [coinbase_tx] + self.tx_pool
        # Reset the current list of transactions
        self.tx_pool = []

        block = dict(header)
        nonce = get_nonce(header, config.TARGET)
        block['nonce'] = nonce
        block['tx'] = txs
        block['hash'] = ''  # TODO caculate block hash
        chain.append(block)


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


def _post(**kwargs):
    try:
        r = requests.post(**kwargs, timeout=5)
        if r.status_code == 200:
            return True, r.json()
    except requests.exceptions.ConnectTimeout as e:
        print(e)
    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.ReadTimeout as e:
        print(e)
    return False, None


def get_chain_from_node(nodes, pub_key):
    if nodes:
        chain = []
        height = 1
        node = nodes[0]
        while True:
            ret, data = _get(url=f'http://{node}/get_block/{height}')
            if ret and data['ok']:
                chain.append(data['block'])
                height += 1
            else:
                break
        if chain:
            return chain

    # Create the genesis block
    print('mining first block')
    block = genesis_block(pub_key)
    return [block]


def get_nodes():
    nodes = set()
    for node in config.DEFAULT_NODES:
        ret, data = _post(url=f'http://{node}/add_node')
        if ret and data['ok']:
            nodes.add(node)
    return list(nodes)


def verify_chain(chain):
    """
    Check required fields, and caculate whole chain from height 1

    :param chain: list of block data
    :return: bool
    """
    pass


def verify_tx(tx):
    """
    Check required fields, and verify account money and signature

    :param tx: dict, tx data
    :return: bool
    """
    pass


def verify_block(block):
    """
    Check required fields, and verify hash, nonce, and target

    :param block: dict, block data
    :return: bool
    """
    pass


def resolve_conflicts():
    pass


def post_data(nodes, type, data):
    """
    Broadcast data to nodes

    :param nodes: list of nodes
    :param type: str, 'tx', 'block', or 'node'
    :param data: a dict, depends on type,
    """
    postfix = f'/add_{type}'
    for node in nodes:
        r = requests.post(url, data)


def genesis_block(pub_key):
    """
    Generate genesis block

    :param pub_key: a address to receive coinbase reward
    :return: a dict of genesis block data
    """
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


def new_tx(sender, recipient, amount):
    tx = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount,
        'ts': time.time(),
    }
    return tx
