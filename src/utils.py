# coding=utf-8
import time
import json

from Crypto.Random.random import randint
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, RIPEMD
import requests
import settings


def new_rsa_key(pvt_key):
    if pvt_key:
        return RSA.importKey(pvt_key.encode())
    # generate 2048bits long key
    return RSA.generate(2048)


def get_hash(inp):
    """
    Creates a SHA-256 hash of a input dictionary

    :param inp: dict, such as block, tx
    """
    b = json.dumps(inp, sort_keys=True).encode()
    h = SHA256.new()
    h.update(b)
    return h.hexdigest()


def get_nonce(header):
    target = header['target']
    while True:
        header = dict(header)
        nonce = randint(0, settings.max_nonce)
        header['nonce'] = nonce
        hash = get_hash(header)
        if hash < target:
            return nonce
        time.sleep(1)  # 1 second


def get_nodes(port):
    nodes = set()
    data = {
        'node': {
            'port': port,
        }
    }
    for node in settings.DEFAULT_NODES:
        ret, info = _post(url=f'http://{node}/add_node', json=data)
        if ret and info['ok']:
            nodes.add(node)
    return list(nodes)


def pub_2_address(pub_key):
    """
    public key-(SHA256)-(RIPEMD160)->public key hash-(base58 encoding)->address

    :param pub_key:
    :return: str, address
    """
    ripemd = RIPEMD.new()
    sha = get_hash(pub_key)
    ripemd.update(sha.encode())
    pub_key_hash = ripemd.hexdigest()
    # TODO base58 encoding
    return pub_key_hash


def base58(inp):
    pass


def _get(**kwargs):
    try:
        r = requests.get(**kwargs, timeout=5)
        if r.status_code == 200:
            return True, r.json()
    except requests.exceptions.ConnectTimeout as e:
        # print(e)
        pass
    except requests.exceptions.ConnectionError as e:
        # print(e)
        pass
    except requests.exceptions.ReadTimeout as e:
        # print(e)
        pass
    return False, None


def _post(**kwargs):
    try:
        r = requests.post(**kwargs, timeout=5)
        if r.status_code == 200:
            return True, r.json()
    except requests.exceptions.ConnectTimeout as e:
        # print(e)
        pass
    except requests.exceptions.ConnectionError as e:
        # print(e)
        pass
    except requests.exceptions.ReadTimeout as e:
        # print(e)
        pass
    except requests.exceptions.InvalidURL as e:
        # print(e)
        pass
    return False, None
