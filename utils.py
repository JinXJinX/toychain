# coding=utf-8
import time
import json
import hashlib
import uuid
from random import randint

import requests
import config


def new_pvt_key():
    return str(uuid.uuid4()).replace('-', '')


def pvt_2_pub_key(pub_key):
    ecdsa = hashlib.new('ecdsa-with-SHA1')
    ecdsa.update(str.encode(pub_key))
    return ecdsa.hexdigest()


def hash(inp):
    """
    Creates a SHA-256 hash of a input dictionary

    :param inp: dict, such as block, tx
    """
    s = json.dumps(inp, sort_keys=True).encode()
    return hashlib.sha256(s).hexdigest()


def get_nonce(header):
    target = header['target']
    max_nonce = 2 ** 32
    while True:
        header = dict(header)
        nonce = randint(0, max_nonce)  # TODO reset max range
        header['nonce'] = nonce
        header_string = json.dumps(header, sort_keys=True).encode()
        hash = hashlib.sha256(header_string).hexdigest()
        if hash < target:
            return nonce
        time.sleep(1)  # 1 second


def get_nodes():
    nodes = set()
    for node in config.DEFAULT_NODES:
        ret, data = _post(url=f'http://{node}/add_node')
        if ret and data['ok']:
            nodes.add(node)
    return list(nodes)


def pub_2_address(pub_key):
    """
    public key-(SHA256)-(RIPEMD160)->public key hash-(base58 encoding)->address

    :param pub_key:
    :return: str, address
    """
    ripemd = hashlib.new('ripemd160')
    sha = hashlib.sha256(pub_key.encode()).hexdigest()
    ripemd.update(sha.encode())
    pub_key_hash = ripemd.hexdigest()
    # TODO base58 encoding
    return ripemd.hexdigest()


def base58(inp):
    pass


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
