# coding=utf-8

import utils
from Crypto.PublicKey import RSA


def pvt_key(inp):
    """
    Check input pvt key is a valid format toychain pvt key

    :param inp: str,
    :return: bool
    """
    pass


def sign(pub_key, tx, signature):
    """

    :param pub_key: b,
    :param msg: b,
    :param signature: int,
    :return: bool
    """
    key = RSA.importKey(pub_key.encode())
    tx2 = {}
    for k in ['from', 'to', 'total_input', 'total_output', 'ts']:
        tx2[k] = tx[k]
    tx_hash = utils.get_hash(tx2)
    return key.verify(tx_hash.encode(), (signature, None))


def chain(chain):
    """
    Check required fields, and caculate whole chain from height 1

    :param chain: list of block data
    :return: bool
    """
    pass


def tx(tx):
    """
    Check required fields, and verify account money and signature

    :param tx: dict, tx data
    :return: bool
    """
    pass


def block(block):
    """
    Check required fields, and verify hash, nonce, and target

    :param block: dict, block data
    :return: bool
    """
    pass
