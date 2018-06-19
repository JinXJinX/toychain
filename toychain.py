# coding=utf-8
import time
import json
import hashlib


toy_chain = []
tx_pool = []
nodes = []
pvt_key = ""


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
        header["nonce"] = nonce
        header_string = json.dumps(header, sort_keys=True).encode()
        hash = hashlib.sha256(header_string).hexdigest()
        if hash < target:
            return nonce
        time.sleep(1)  # 1 second


def verify_chain():
    pass


def verify_tx():
    pass


def verify_block():
    pass


def resolve_conflicts():
    pass


def post_data(type, data):
    postfix = f"/add_{type}"
    for node in nodes:
        r = requests.post(url, data)


def post_tx(tx):
    return post_data("tx", tx)


def post_block(block):
    return post_data("block", block)


def post_node(node):
    return post_data("node", node)


def new_block():
    header = {
        'index': len(toychain) + 1,
        'timestamp': time(),
        'previous_hash': previous_hash or hash(self.chain[-1]),
    }
    coinbase_tx = new_tx("", self.pub_key, 50)
    txs = [coinbase_tx] + self.tx_pool
    # Reset the current list of transactions
    tx_pool = []

    block = dict(header)
    nonce = get_nonce(header, settings.target)
    block['nonce'] = nonce
    block['tx'] = txs


def new_tx(sender, recipient, amount):
    tx = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
        "ts": time.time(),
    }
    return tx
